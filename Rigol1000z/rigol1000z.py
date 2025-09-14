import os
import numpy as _np
import tqdm as _tqdm
import pyvisa as _visa

class _Rigol1000zChannel:
    '''
    Handles the channels configuration (vertical axis).
    '''

    def __init__(self, channel, osc):
        self._channel = channel
        self._osc = osc

    def visa_write(self, cmd):
        return self._osc.visa_write(':chan%i%s' % (self._channel, cmd))

    def visa_read(self):
        return self._osc.visa_read()

    def visa_ask(self, cmd):
        self.visa_write(cmd)
        r = self.visa_read()
        return r

    def get_voltage_rms_V(self):
        assert 1 <= self._channel <= 4, 'Invalid channel.'
        return self._osc.ask(':MEAS:ITEM? VRMS,CHAN%i' % self._channel)

    def select_channel(self):
        self._osc.write(':MEAS:SOUR CHAN%i' % self._channel)
        return self._osc.selected_channel()

    def get_coupling(self):
        return self.visa_ask(':coup?')

    def set_coupling(self, coupling):
        coupling = coupling.upper()
        assert coupling in ('AC', 'DC', 'GND')
        self.visa_write(':coup %s' % coupling)
        return self.get_coupling()

    def enable(self):
        self.visa_write(':disp 1' % self._channel)
        return self.enabled()

    def disable(self):
        self.visa_write(':disp 0' % self._channel)
        return self.disabled()

    def enabled(self):
        return bool(int(self.visa_ask(':disp?')))

    def disabled(self):
        return bool(int(self.visa_ask(':disp?'))) ^ 1

    def get_offset_V(self):
        return float(self.visa_ask(':off?'))

    def set_offset_V(self, offset):
        assert -1000 <= offset <= 1000.
        self.visa_write(':off %.4e' % offset)
        return self.get_offset_V()

    def get_range_V(self):
        return self.visa_ask(':rang?')

    def set_range_V(self, range):
        assert 8e-3 <= range <= 800.
        self.visa_write(':rang %.4e' % range)
        return self.get_range_V()

    def set_vertical_scale_V(self, scale):
        assert 1e-3 <= scale <= 100
        self.visa_write(':scal %.4e' % scale)

    def get_probe_ratio(self):
        return float(self.visa_ask(':prob?'))

    def set_probe_ratio(self, ratio):
        assert ratio in (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1,\
                         2, 5, 10, 20, 50, 100, 200, 500, 1000)
        self.visa_write(':prob %s' % ratio)
        return self.get_probe_ratio()

    def get_units(self):
        return self.visa_ask(':unit?')

    def set_units(self, unit):
        unit = unit.lower()
        assert unit in ('volt', 'watt', 'amp', 'unkn')
        self.visa_write(':unit %s' % unit)

    def get_data_premable(self):
        '''
        Get information about oscilloscope axes.

        Returns:
            dict: A dictionary containing general oscilloscope axes information.
        '''
        pre = self._osc.visa_ask(':wav:pre?').split(',')
        pre_dict = {
            'format': int(pre[0]),
            'type': int(pre[1]),
            'points': int(pre[2]),
            'count': int(pre[3]),
            'xincrement': float(pre[4]),
            'xorigin': float(pre[5]),
            'xreference': float(pre[6]),
            'yincrement': float(pre[7]),
            'yorigin': float(pre[8]),
            'yreference': float(pre[9]),
        }
        return pre_dict

    def get_data(self, mode='norm', filename=None):
        '''
        Download the captured voltage points from the oscilloscope.

        Args:
            mode (str): 'norm' if only the points on the screen should be
                downloaded, and 'raw' if all the points the ADC has captured
                should be downloaded.  Default is 'norm'.
            filename (None, str): Filename the data should be saved to.  Default
                is `None`; the data is not saved to a file.

        Returns:
            2-tuple: A tuple of two lists.  The first list is the time values
                and the second list is the voltage values.

        '''
        assert mode in ('norm', 'raw')

        # Setup scope
        self._osc.visa_write(':stop')
        self._osc.visa_write(':wav:sour chan%i' % self._channel)
        self._osc.visa_write(':wav:mode %s' % mode)
        self._osc.visa_write(':wav:form byte')

        info = self.get_data_premable()

        max_num_pts = 250000
        num_blocks = info['points'] // max_num_pts
        last_block_pts = info['points'] % max_num_pts

        datas = []
        for i in _tqdm.tqdm(range(num_blocks+1), ncols=60):
            if i < num_blocks:
                self._osc.visa_write(':wav:star %i' % (1+i*250000))
                self._osc.visa_write(':wav:stop %i' % (250000*(i+1)))
            else:
                if last_block_pts:
                    self._osc.visa_write(':wav:star %i' % (1+num_blocks*250000))
                    self._osc.visa_write(':wav:stop %i' % (num_blocks*250000+last_block_pts))
                else:
                    break
            data = self._osc.visa_ask_raw(':wav:data?')[11:]
            data = _np.frombuffer(data, 'B')
            datas.append(data)

        datas = _np.concatenate(datas)
        v = (datas - info['yorigin'] - info['yreference']) * info['yincrement']
        
        print(v)
        
        v = v[:info['points']] # In case we got more data than expected.
        print(v)
        
        print(f"data points: {len(datas)}, expected: {info['points']}") 
        print(f"v points: {len(v)}, expected: {info['points']}") 

        t = _np.arange(0, info['points']*info['xincrement'], info['xincrement'])
        
        print(f"t points: {len(t)}, expected: {info['points']}")
        print(len(t), info['points'])
        
        assert len(v) == info['points']

        assert len(t) == info['points']
        # info['xorigin'] + info['xreference']

        if filename:
            try:
                os.remove(filename)
            except OSError:
                pass
            _np.savetxt(filename, _np.c_[t, v], '%.12e', ',')

        return t, v

class _Rigol1000zTrigger:
    '''
    Handles the trigger configuration.
    '''

    def __init__(self, osc):
        self._osc = osc

    def get_trigger_level_V(self):
        return self._osc.visa_ask(':trig:edg:lev?')

    def set_trigger_level_V(self, level):
        self._osc.visa_write(':trig:edg:lev %.3e' % level)
        return self.get_trigger_level_V()

    def get_trigger_holdoff_s(self):
        return self._osc.visa_ask(':trig:hold?')

    def set_trigger_holdoff_s(self, holdoff):
        self._osc.visa_write(':trig:hold %.3e' % holdoff)
        return self.get_trigger_holdoff_s()

class _Rigol1000zTimebase:
    '''
    Handles the timebase configuration (horizontal axis).
    '''

    def __init__(self, osc):
        self._osc = osc

    def visa_write(self, cmd):
        return self._osc.visa_write(':tim%s' % cmd)

    def visa_read(self):
        return self._osc.visa_read()

    def visa_ask(self, cmd):
        self.visa_write(cmd)
        r = self.visa_read()
        return r

    def get_timebase_scale_s_div(self):
        return float(self.visa_ask(':scal?'))

    def set_timebase_scale_s_div(self, timebase):
        assert 50e-9 <= timebase <= 50
        self.visa_write(':scal %.4e' % timebase)
        return self.get_timebase_scale_s_div()

    def get_timebase_mode(self):
        return self.visa_ask(':mode?')

    def set_timebase_mode(self, mode):
        mode = mode.lower()
        assert mode in ('main', 'xy', 'roll')
        self.visa_write(':mode %s' % mode)
        return self.get_timebase_mode()

    def get_timebase_offset_s(self):
        return self.visa_ask(':offs?')

    def set_timebase_offset_s(self, offset):
        self.visa_write(':offs %.4e' % -offset)
        return self.get_timebase_offset_s()

class Rigol1000z:
    '''
    Rigol DS1000z series oscilloscope driver.

    Channels 1 through 4 (or 2 depending on the oscilloscope model) are accessed
    using `[channel_number]`.  e.g. osc[2] for channel 2.  Channel 1 corresponds
    to index 1 (not 0).

    Attributes:
        trigger (`_Rigol1000zTrigger`): Trigger object containing functions
            related to the oscilloscope trigger.
        timebase (`_Rigol1000zTimebase`): Timebase object containing functions
            related to the oscilloscope timebase.
    '''

    def __init__(self, visa_resource):
        self.visa_resource = visa_resource

        self._channels = [_Rigol1000zChannel(c, self) for c in range(1,5)]
        self.trigger = _Rigol1000zTrigger(self)
        self.timebase = _Rigol1000zTimebase(self)

    def __getitem__(self, i):
        assert 1 <= i <= 4, 'Not a valid channel.'
        return self._channels[i-1]

    def __len__(self):
        return len(self._channels)

    def visa_write(self, cmd):
        self.visa_resource.write(cmd)

    def visa_read(self):
        return self.visa_resource.read().strip()

    # https://github.com/jeanyvesb9/Rigol1000z/pull/2
    # This argument is ultimately passed to the _read_raw function in pyvisa, for which the default argument is None. 
    # Source: https://github.com/pyvisa/pyvisa/blob/main/pyvisa/resources/messagebased.py?rgh-link-date=2021-02-14T01%3A37%3A37Z#L407-L453
    # https://github.com/pyvisa/pyvisa/blob/908d8674478d5b1034b7b5a140afb990e1505392/pyvisa/resources/messagebased.py#L407-L453
    def visa_read_raw(self, num_bytes=None):
        return self.visa_resource.read_raw(num_bytes)

    def visa_ask(self, cmd):
        return self.visa_resource.query(cmd)

    # https://github.com/jeanyvesb9/Rigol1000z/pull/2
    # This argument is ultimately passed to the _read_raw function in pyvisa, for which the default argument is None. 
    # Source: https://github.com/pyvisa/pyvisa/blob/main/pyvisa/resources/messagebased.py?rgh-link-date=2021-02-14T01%3A37%3A37Z#L407-L453
    # https://github.com/pyvisa/pyvisa/blob/908d8674478d5b1034b7b5a140afb990e1505392/pyvisa/resources/messagebased.py#L407-L453
    def visa_ask_raw(self, cmd, num_bytes=None):
        self.visa_write(cmd)
        return self.visa_read_raw(num_bytes)

    def autoscale(self):
        self.visa_write(':aut')

    def clear(self):
        self.visa_write(':clear')

    def run(self):
        self.visa_write(':run')

    def stop(self):
        self.visa_write(':stop')

    def force(self):
        self.visa_write(':tfor')

    def set_single_shot(self):
        self.visa_write(':sing')

    def get_id(self):
        return self.visa_ask('*IDN?')

    def get_averaging(self):
        return self.visa_ask(':acq:aver?')

    def set_averaging(self, count):
        assert count in [2**n for n in range(1, 11)]
        self.visa_write(':acq:aver %i' % count)
        return self.get_averaging()

    def set_averaging_mode(self):
        self.visa_write(':acq:type aver')
        return self.get_mode()

    def set_normal_mode(self):
        self.visa_write(':acq:type norm')
        return self.get_mode()

    def set_high_resolution_mode(self):
        self.visa_write(':acq:type hres')
        return self.get_mode()

    def set_peak_mode(self):
        self.visa_write(':acq:type peak')
        return self.get_mode()

    def get_mode(self):
        modes = {
            'NORM': 'normal',
            'AVER': 'averages',
            'PEAK': 'peak',
            'HRES': 'high_resolution'
        }
        return modes[self.visa_ask(':acq:type?')]

    def get_sampling_rate(self):
        return float(self.visa_ask(':acq:srat?'))

    def get_memory_depth(self):
        md = self.visa_ask(':acq:mdep?')

        return int(md) if md != 'AUTO' else md

    def set_memory_depth(self, pts):
        num_enabled_chans = sum(self.get_channels_enabled())
        
        pts = int(pts) if pts != 'AUTO' else pts

        if num_enabled_chans == 1:
            assert pts in ('AUTO', 12000, 120000, 1200000, 12000000, 24000000)
        elif num_enabled_chans == 2:
            assert pts in ('AUTO', 6000, 60000, 600000, 6000000, 12000000)
        elif num_enabled_chans in (3, 4):
            assert pts in ('AUTO', 3000, 30000, 300000, 3000000, 6000000)

        self.run()
        self.visa_write(':acq:mdep %s' % pts)
        
    def get_channels_enabled(self):
        return [c.enabled() for c in self._channels]

    def selected_channel(self):
        return self.visa_ask(':MEAS:SOUR?')

    def get_screenshot(self, filename = None, format='png'):
        '''
        Downloads a screenshot from the oscilloscope.

        Args:
            filename (str): The name of the image file.  The appropriate
                extension should be included (i.e. jpg, png, bmp or tif).
            type (str): The format image that should be downloaded.  Options
                are 'jpeg, 'png', 'bmp8', 'bmp24' and 'tiff'.  It appears that
                'jpeg' takes <3sec to download while all the other formats take
                <0.5sec.  Default is 'png'.
        '''

        assert format in ('jpeg', 'png', 'bmp8', 'bmp24', 'tiff')

        #Due to the up to 3s delay, we are setting timeout to None for this operation only
        oldTimeout = self.visa_resource.timeout
        self.visa_resource.timeout = None

        raw_img = self.visa_ask_raw(':disp:data? on,off,%s' % format, 3850780)[11:-4]

        self.visa_resource.timeout = oldTimeout

        if filename:
            try:
                os.remove(filename)
            except OSError:
                pass
            with open(filename, 'wb') as fs:
                fs.write(raw_img)

        return raw_img