"""
    Main program from which sub-functions are called to run the final algorithm
"""

# import files #
from data_management import *       # import, track, and clean data
# from data_scrape import *           # real-time stock data
from regression import *            # run regression w/ gradient descent
# from performance_sim import *       # simulate the performance of the final model
from visualize import *             # plotting regressive looks
from math import floor              # time split


# set params #
global dir
dir = "./NYSE_sample_data/prices_adjusted.csv"
global weight_distribution
weight_distribution = [10, 10, 15, 25, 15, 10, 5]
global time_frame_ratio
time_frame_ratio = [1, .75, .5, .25, .1, .05, .01]
global current_price
current_price = -1.0


# conduct algorithm #
def main():
    # declare vars #
    regr_looks = []
    regr_preds = []

    # import #
    dataset = data_import(dir)
    col_labels = dataset[0]

    data = dataset[1]
    exp_output = dataset[2]

    test_data = dataset[3]
    test_exp_output = dataset[4]
    
    cv_data = dataset[5]
    cv_exp_output = dataset[6]
    
    global current_price
    current_price = dataset[7]

    # time frames #
    data[np.atleast_2d(data)[:, 0].argsort()]
    time_frames = split_time_frame(data, time_frame_ratio)
    
    # train models #
    for frame in time_frames:
        # add trained model #
        regr_looks += [ optimize(np.atleast_2d(data)[ : frame, : ], exp_output[ : frame])[1 : ] ]

    # multi-regressive model #
    multi_regr = regr_weighted(regr_looks, weight_distribution)
    
    # predictions #
        # regr_preds = regr_prediction(regr_looks, test_data)
    print(multi_regr.coef_)
    print(multi_regr.intercept_)
    regr_preds = multi_regr.predict(test_data)

    # visualize #
    # print("VISUALIZING")
    # fig, axs = plot_whole(regr_preds, test_data, test_exp_output, col_labels)
    # plt.show()


# weighted distribution of regressive looks #
def regr_weighted(regr_looks, weight_distribution):
    # apply weighting #
    multi_coef = []
    for look_num in range(len(regr_looks)):
        multi_coef += [ weight_distribution[look_num] * coef for coef in regr_looks[look_num][0] ]
    
    # averaging #
        # multi_coef = np.average(regr_looks[ : , 0], weight_distribution)
    multi_coef = np.asarray(multi_coef).mean(axis=0)

    # return model #
    multi_regr = linear_model.LinearRegression()
    multi_regr.coef_ = multi_coef
    multi_regr.intercept_ = current_price
    return multi_regr


# create custom weighting based on predictive range #
def distribute_weights(pred_range, skew, num_timeframes):
    """
        pred_range: number of time units to predict to
        skew:       -1 is left (longer term) skew,
                    0 is normal curve,
                    1 is right (shorter term skew)
    """
    # to be implemented #
    return weight_distribution


# divide data into time frames #
def split_time_frame(time_data, frame_ratio):
    # range #
    begin = np.min(time_data)
    end = np.max(time_data)
    range = end - begin

    # divide #
    return [floor(ratio * range) for ratio in frame_ratio]

if __name__ == "__main__":
    main()