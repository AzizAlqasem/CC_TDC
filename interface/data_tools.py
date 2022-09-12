from settings.settings import settings
import numpy as np
import numba

def raw_data_to_channel_arr(
        data:list, channel_size=settings.get_setting("tot_nodch"),
        marker_size=settings.get_setting("marker_size"),
        smarker=settings.get_setting("start_marker"),
        emarker=settings.get_setting("end_marker")):
    number_of_data_chunck = data[0] # = number of laser shot
    # print(number_of_data_chunck, len(data)) #= 227, 4088
    assert data[-1] == emarker, f"{data}"
    data_ar = np.array(data[1:-1], dtype=np.int32).reshape(number_of_data_chunck,
                         channel_size + marker_size)
    assert np.all(data_ar[:,0]==smarker)
    assert np.all(data_ar[:,-1]==emarker)
    return data_ar[:,1:-1]


@numba.jit(nopython=True)
def channel_arr_to_count_ar(channel_arr, min_count_value=1, max_count_value=2048):
    # the channel_arr is a 2D array with shape (number_of_data_chunck, channel_size)
    # it contains the index numbers that correspond to the hit times
    # Example: for 1 ns resoultion TDC, index at 10 ~= 10 ns
    data_ar = channel_arr.flatten()
    cond = (data_ar>=min_count_value) & (data_ar<max_count_value)   # [min, ..., max)
    data_ar = data_ar[cond] # this will prodec (mostally) a new sized array with indeces that are in the range [min, ..., max)
    return _count_to_bins(data_ar, size=max_count_value - min_count_value), data_ar.size


@numba.jit(nopython=True)
def _count_to_bins(data_ar, size):
    count_ar = np.zeros(size, dtype=np.int32)#np.zeros(size, dtype=np.int64)
    for bin in data_ar:  #i in range(len(data_ar)):
        # bin = data_ar[i]#data_ar[i]
        count_ar[bin-1] += 1
    return count_ar