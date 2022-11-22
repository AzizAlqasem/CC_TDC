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
        #* Potential bug*
        # The 1 in bin-1 is because the min_count_value is 1 and not 0
        # But that not always the case, so we need to check if the min_count_value is 1
    return count_ar



# mesure the time distence between to peaks (within the same laser shot)
@numba.jit(nopython=True)
def get_time_distence_between_peaks(diff_arr, char1, char2, min_count_value=1, max_count_value=2048):
    for i in range(char1.shape[0]):
        ch1 = char1[i]
        ch2 = char2[i]
        if ch1 >= min_count_value and ch1 < max_count_value and ch2 >= min_count_value and ch2 < max_count_value:
            diff_arr[ch2-ch1] += 1
    return diff_arr



# @numba.jit(nopython=True)
# def get_time_distence_between_peaks(channel_arr, min_count_value=1, max_count_value=2048):
#     size = max_count_value - min_count_value
#     diff_1_arr = np.zeros(size, dtype=np.int32)
#     # diff_2_arr = np.zeros(size, dtype=np.int32)
#     for i in range(channel_arr.shape[0]):
#         ch1 = channel_arr[i,0]
#         ch2 = channel_arr[i,1]
#         # ch3 = channel_arr[i,2]
#         if ch1 >= min_count_value and ch1 < max_count_value and ch2 >= min_count_value and ch2 < max_count_value:
#             diff1 = ch2 - ch1
#             diff_1_arr[diff1] += 1
#             # if ch3 >= min_count_value and ch3 < max_count_value:
#             #     diff2 = ch3 - ch2
#             #     diff_2_arr[diff2] += 1
#     return diff_1_arr  #, diff_2_arr


