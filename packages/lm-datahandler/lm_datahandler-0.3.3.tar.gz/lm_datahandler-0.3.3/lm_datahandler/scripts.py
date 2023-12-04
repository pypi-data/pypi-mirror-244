import os.path
import sys
import numpy as np
import lightgbm as lgb
import scipy.signal as sp_sig
from scipy import signal
from scipy.integrate._quadrature import simps
from scipy.io import loadmat

from lm_datahandler.data_download.data_download import download_lm_data_from_server
from lm_datahandler.datahandler import DataHandler
import pandas as pd

from lm_datahandler.function_in_test.other_features import generate_cluster_feature1, generate_cluster_feature2, \
    generate_cluster_feature3


def download_and_full_analyse(download_params, analyse_param=None):
    data_save_path = download_params["save_path"]
    data_list = download_lm_data_from_server(download_params, data_save_path)

    analysis_save_path = download_params["analysis_save_path"]

    local_datas_full_analyse(data_save_path, data_list, analysis_save_path=analysis_save_path,
                             analyse_param=analyse_param)


def local_datas_full_analyse(data_path, data_names, analysis_save_path=None, analyse_param=None):
    assert os.path.exists(data_path), "The input dir path does not exist."

    if analyse_param is None:
        device_type = 'X7'
        data_type = "sleep"
        pre_process_param = {'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]},
        parse_to_mat = True
        show_plots = False
        plot_sw_stim_sham = True
        plot_sleep_fig = True
    else:
        device_type = analyse_param['device_type']
        data_type = analyse_param["data_type"]
        pre_process_param = analyse_param["pre_process_param"]
        parse_to_mat = analyse_param["parse_to_mat"]
        show_plots = analyse_param["show_plots"]
        plot_sw_stim_sham = analyse_param["plot_sw_stim_sham"]
        plot_sleep_fig = analyse_param["plot_sleep_fig"]

    if analysis_save_path is None:
        analysis_save_path = data_path
    else:
        if not os.path.exists(analysis_save_path):
            os.mkdir(analysis_save_path)
    if data_names is None:
        data_names = os.listdir(data_path)
    for i, data_name in enumerate(data_names):
        print("Start analysis data: {}".format(data_name))
        if not (os.path.exists(os.path.join(data_path, data_name + "/eeg.eeg")) or os.path.exists(
                os.path.join(data_path, data_name + "/eeg.qle"))):
            print("data: \"{}\" not found, skipped.".format(data_name))
            continue
        try:

            data_handler = DataHandler()

            temp_data_path = os.path.join(data_path, data_name)

            data_analysis_save_path = os.path.join(analysis_save_path, data_name)

            if not os.path.exists(data_analysis_save_path):
                os.mkdir(data_analysis_save_path)
            sleep_fig_save_path = os.path.join(data_analysis_save_path, "sleep_fig.png")
            slow_wave_stim_sham_plot = os.path.join(data_analysis_save_path, "sw_stim_sham_fig.png")

            analysis_results_save_path = os.path.join(data_analysis_save_path, "analysis_results.xlsx")

            analysis_report_save_path = os.path.join(data_analysis_save_path, data_name + "_sleep_report.pdf")

            # 数据加载
            patient_info = {"phone_number": data_name[0:11]}
            data_handler.load_data(device_type=device_type, data_name=data_name, data_path=temp_data_path, patient_info=patient_info)
            if parse_to_mat:
                data_handler.save_data_to_mat(os.path.join(data_analysis_save_path, "eeg_and_acc.mat"))

            if data_type == "sleep":
                # 绘制慢波增强对比图，并保存
                if plot_sw_stim_sham:
                    data_handler.plot_sw_stim_sham(savefig=slow_wave_stim_sham_plot)

                # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
                data_handler.preprocess(filter_param=pre_process_param).sleep_staging(use_acc=True)
                # if os.path.exists(os.path.join(temp_data_path, "hypno.mat")):
                #     hypno = loadmat(os.path.join(temp_data_path, "hypno.mat"))["manual"]
                #     data_handler.sleep_staging_result = np.squeeze(hypno)
                data_handler.compute_sleep_variables()

                if plot_sleep_fig:
                    data_handler.plot_sleep_data(savefig=sleep_fig_save_path)

                # data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': 70, 'bandstop': [
                #     [49, 51]]}).sleep_staging().compute_sleep_variables()
                # features = generate_cluster_feature1(data_handler)
                # features_df = pd.DataFrame(features)
                # features_df.to_csv(os.path.join(data_analysis_save_path, "absolute_power.csv"), index=True)
                #
                # features = generate_cluster_feature2(data_handler)
                # features_df = pd.DataFrame(features)
                # features_df.to_csv(os.path.join(data_analysis_save_path, "relative_power.csv"), index=True)
                #
                # features = generate_cluster_feature3(data_handler)
                # features_df = pd.DataFrame(features)
                # features_df.to_csv(os.path.join(data_analysis_save_path, "beta_abnormal_percentage.csv"), index=True)

                # spindle检测和慢波检测
                data_handler.sw_detect()
                data_handler.spindle_detect()

                # data_handler.plot_sp_results_by_id(60, range=5000, savefig=os.path.join(data_analysis_save_path, "sp_no.{}.png".format(50)))
                # data_handler.plot_sw_results_by_id(50, range=5000, savefig=os.path.join(data_analysis_save_path, "sw_no.{}.png".format(50)))

                # 导出结果成excel
                data_handler.export_analysis_result_to_xlsx(analysis_results_save_path, sw_results=True,
                                                            sp_results=True,
                                                            sleep_variables=True)
            elif data_type == "anes":
                # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
                data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': None, 'bandstop': [
                    [49, 51]]}).sleep_staging(use_acc=True).compute_sleep_variables().plot_anes_data(
                    savefig=sleep_fig_save_path)

            if show_plots:
                data_handler.show_plots()

            data_handler.export_analysis_report(analysis_report_save_path)


        except AssertionError as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("AssertionError: {}".format(e))
            print("File: {}".format(exc_traceback.tb_frame.f_code.co_filename))
            print("Line Number: {}".format(exc_traceback.tb_lineno))
            print("当前数据出错，将跳过当前数据.")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Unknown Error: {}".format(e))
            print("File: {}".format(exc_traceback.tb_frame.f_code.co_filename))
            print("Line Number: {}".format(exc_traceback.tb_lineno))
            print("当前数据出错，将跳过当前数据.")
        finally:

            continue


def local_data_concat_and_analyse(data_path, data_names, analysis_save_path=None, analyse_param=None):
    assert os.path.exists(data_path), "The input dir path does not exist."

    if analyse_param is None:
        data_type = "sleep"
        pre_process_param = {'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]},
        parse_to_mat = True
        show_plots = False
        plot_sw_stim_sham = True
        plot_sleep_fig = True
    else:
        data_type = analyse_param["data_type"]
        pre_process_param = analyse_param["pre_process_param"]
        parse_to_mat = analyse_param["parse_to_mat"]
        show_plots = analyse_param["show_plots"]
        plot_sw_stim_sham = analyse_param["plot_sw_stim_sham"]
        plot_sleep_fig = analyse_param["plot_sleep_fig"]

    data_handler = DataHandler()

    for i in range(len(data_names)):
        # 数据加载
        if i == 0:
            patient_info = {"phone_number": data_names[i][0:11]}
            data_handler.load_data(data_name=data_names[0], data_path=os.path.join(data_path, data_names[i]),
                                   patient_info=patient_info)
        else:
            data_handler.concat_data(data_path=os.path.join(data_path, data_names[i]))

    data_name = data_handler.data_name

    data_analysis_save_path = os.path.join(analysis_save_path, data_name)

    if not os.path.exists(data_analysis_save_path):
        os.mkdir(data_analysis_save_path)
    sleep_fig_save_path = os.path.join(data_analysis_save_path, "sleep_fig.png")
    slow_wave_stim_sham_plot = os.path.join(data_analysis_save_path, "sw_stim_sham_fig.png")

    analysis_results_save_path = os.path.join(data_analysis_save_path, "analysis_results.xlsx")

    analysis_report_save_path = os.path.join(data_analysis_save_path, "sleep_report.pdf")

    if parse_to_mat:
        data_handler.save_data_to_mat(os.path.join(data_analysis_save_path, "eeg_and_acc.mat"))

    if data_type == "sleep":
        # 绘制慢波增强对比图，并保存
        if plot_sw_stim_sham:
            data_handler.plot_sw_stim_sham(savefig=slow_wave_stim_sham_plot)

        # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
        data_handler.preprocess(filter_param=pre_process_param).sleep_staging(use_acc=True)
        # if os.path.exists(os.path.join(temp_data_path, "hypno.mat")):
        #     hypno = loadmat(os.path.join(temp_data_path, "hypno.mat"))["manual"]
        #     data_handler.sleep_staging_result = np.squeeze(hypno)
        data_handler.compute_sleep_variables()

        if plot_sleep_fig:
            data_handler.plot_sleep_data(savefig=sleep_fig_save_path)

        # data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': 70, 'bandstop': [
        #     [49, 51]]}).sleep_staging().compute_sleep_variables()
        # features = generate_cluster_feature1(data_handler)
        # features_df = pd.DataFrame(features)
        # features_df.to_csv(os.path.join(data_analysis_save_path, "absolute_power.csv"), index=True)
        #
        # features = generate_cluster_feature2(data_handler)
        # features_df = pd.DataFrame(features)
        # features_df.to_csv(os.path.join(data_analysis_save_path, "relative_power.csv"), index=True)
        #
        # features = generate_cluster_feature3(data_handler)
        # features_df = pd.DataFrame(features)
        # features_df.to_csv(os.path.join(data_analysis_save_path, "beta_abnormal_percentage.csv"), index=True)

        # spindle检测和慢波检测
        data_handler.sw_detect()
        data_handler.spindle_detect()

        # 导出结果成excel
        data_handler.export_analysis_result_to_xlsx(analysis_results_save_path, sw_results=True,
                                                    sp_results=True,
                                                    sleep_variables=True)
    elif data_type == "anes":
        # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
        data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': None, 'bandstop': [
            [49, 51]]}).sleep_staging().compute_sleep_variables().plot_anes_data(
            savefig=sleep_fig_save_path)

    if show_plots:
        data_handler.show_plots()

    data_handler.export_analysis_report(analysis_report_save_path)


def compute_sleep_variables_from_hypno(hypno):
    data_handler = DataHandler()
    data_handler.compute_sleep_variables(hypno)
    sleep_variables_df = {
        "TST(H)": [data_handler.sleep_variables["TST"] / 3600],
        "SOL(H)": [data_handler.sleep_variables["SOL"] / 3600],
        "GU(H)": [data_handler.sleep_variables["GU"] / 3600],
        "WASO(M)": [data_handler.sleep_variables["WASO"] / 60],
        "SE(%)": [data_handler.sleep_variables["SE"] * 100],
        "AR": [data_handler.sleep_variables["AR"]],
        "N3(H)": [data_handler.sleep_variables["N3"] / 3600],
        "N12(H)": [data_handler.sleep_variables["N12"] / 3600],
        "REM(H)": [data_handler.sleep_variables["REM"] / 3600],
        "Hypno": [data_handler.sleep_variables["HYPNO"]]
    }
    print(sleep_variables_df)


def bandpower_from_psd_ndarray(bands, psd, freqs, relative=True):
    # Type checks
    assert isinstance(bands, list), "bands must be a list of tuple(s)"
    assert isinstance(relative, bool), "relative must be a boolean"

    # Safety checks
    freqs = np.asarray(freqs)
    psd = np.asarray(psd)
    assert freqs.ndim == 1, "freqs must be a 1-D array of shape (n_freqs,)"
    assert psd.shape[-1] == freqs.shape[-1], "n_freqs must be last axis of psd"

    # Extract frequencies of interest
    all_freqs = np.hstack([[b[0], b[1]] for b in bands])
    fmin, fmax = min(all_freqs), max(all_freqs)
    idx_good_freq = np.logical_and(freqs >= fmin, freqs <= fmax)
    freqs = freqs[idx_good_freq]
    res = freqs[1] - freqs[0]

    # Trim PSD to frequencies of interest
    psd = psd[..., idx_good_freq]

    # plt.imshow(psd.T[:50,:], cmap='jet')
    # plt.show()
    # assert 0

    # Check if there are negative values in PSD
    if (psd < 0).any():
        pass

    # Calculate total power
    total_power = simps(psd, dx=res, axis=-1)
    total_power = total_power[np.newaxis, ...]

    # Initialize empty array
    bp = np.zeros((len(bands), *psd.shape[:-1]), dtype=np.float64)

    # Enumerate over the frequency bands
    labels = []
    for i, band in enumerate(bands):
        b0, b1, la = band
        labels.append(la)
        idx_band = np.logical_and(freqs >= b0, freqs <= b1)
        bp[i] = simps(psd[..., idx_band], dx=res, axis=-1)

    if relative:
        bp /= total_power

    all_freqs = all_freqs.reshape(-1, 2)
    total_bands = all_freqs[:, 1] - all_freqs[:, 0]
    total_bands = total_bands[..., np.newaxis]
    bp /= total_bands
    return bp


if __name__ == '__main__':
    start_day = '20231130'
    end_day = '20231130'
    download_param = {
        # 正式服：http://8.136.42.241/， 测试服：http://150.158.153.12/
        'url': 'http://http://8.136.42.241/:38083/inner/filter',
        # 刺激范式：1. 手动刺激，2. 音频刺激，3. N3闭环刺激，4. 纯记录模式，5. 记录模式， 6. 音频刺激
        'paradigms': None,
        # 用户手机号
        'phones': [15777799719],
        # 基座mac
        'macs': None,
        # 服务版本
        'serviceVersions': None,
        # 睡眠主观评分，1~5，-1表示未评分
        'sleepScores': None,
        # 停止类型， 0. 断连超时, 1. 用户手动, 2. 头贴放到基座上停止, 3. 关机指令触发, 4. 低电量, 5. 崩溃
        'stopTypes': None,
        # 时间范围，以停止记录的时间为准
        'dateRange': [str(start_day), str(end_day)],
        # 数据时长范围
        'dataLengthRange': [60 * 3 * 60, 60 * 12 * 60],
        # 翻身次数范围
        'turnoverCountRange': None,
        # 刺激次数范围
        'stimulationCountRange': None,
        # 下载保存路径
        'save_path': os.path.join('E:/dataset/x7_tail', "{}_{}".format(start_day, end_day)),
        # 分析结果保存路径（为None表示保存在数据下载路径中）
        'analysis_save_path': os.path.join('E:/dataset/x7_tail', "{}_{}".format(start_day, end_day)),
    }
    analyse_param = {
        # 设备类型：X7/X8
        'device_type': "X8",
        # 数据类型：sleep(睡眠数据) / anes(麻醉数据)
        'data_type': "sleep",
        # 滤波参数，一般不需要改动
        'pre_process_param': {'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]},
        # 是否额外保存数据成.mat格式
        'parse_to_mat': True,
        # 是否显示matplotlib绘图，一般不推荐
        'show_plots': False,
        # 是否绘制慢波增强对比图(ERP图)
        'plot_sw_stim_sham': True,
        # 是否绘制睡眠分期图
        'plot_sleep_fig': True
    }
    # 在线下载并分析
    # download_and_full_analyse(download_param, analyse_param)

    # 直接本地分析
    local_datas_full_analyse(r'E:\dataset\dev_test_data',
                             ['18785524802_1202-19_27_53_1203-00_02_50_-0.00_5'],
                             r'E:\dataset\dev_test_data', analyse_param=analyse_param)

    # df = pd.read_parquet("E:/githome/lm_datahandler/lm_datahandler/train/realtime_eeg_acc_20231117.parquet")
    # df.drop(["acc_diff_avg_ratio", "acc_diff_avg_ratio_p2min_norm"], axis=1, inplace=True)
    # df.to_parquet("E:/githome/lm_datahandler/lm_datahandler/train/realtime_eeg_acc_20231117.parquet")




    # data = loadmat(r"E:\dataset\X7-PSG\JZ_data\label_and_prediction\final_data\20230520_WZY\eeg_and_acc.mat")
    # eeg = data["eeg"].squeeze()
    # acc = (data["acc"] - 32767)
    # eeg_epoch = eeg.shape[0] // 7500
    # acc_epoch = acc.shape[1] // 750
    # assert eeg_epoch == acc_epoch, "EEG Length not Consistent with ACC"
    # eeg = eeg[0: eeg_epoch*7500]
    # acc = acc[:, 0: acc_epoch*750]
    #
    # wn_h = 2 * 0.5 / 500
    # b_h, a_h = signal.butter(3, wn_h, 'highpass', analog=False)
    # zi_h = signal.lfilter_zi(b_h, a_h)
    #
    # w0_b = 49 / (500 / 2)
    # w1_b = 51 / (500 / 2)
    # b_b, a_b = signal.butter(3, [w0_b, w1_b], btype='bandstop', analog=False)
    # zi_b = signal.lfilter_zi(b_b, a_b)
    #
    #
    # clf = lgb.Booster(
    #     model_file=r'E:\githome\lm_datahandler\lm_datahandler\train\realtime_sleepstaging_15s_eeg_acc_120iter_20231120_214814.txt')
    #
    # feature_names = clf.feature_name()
    # raw_feature_names = [item for item in feature_names if not item.endswith("norm")]
    # # eeg = signal.lfilter(b, a, eeg, zi=zi)
    # sleep_stage_results = []
    # cached_feature = None
    # for i in range(eeg_epoch):
    #     eeg_i = eeg[i * 7500: (i+1) * 7500]
    #     acc_i = acc[:, i * 750: (i+1) * 750]
    #     eeg_i, zi_b = signal.lfilter(b_b, a_b, eeg_i, zi=zi_b)
    #     eeg_i, zi_h = signal.lfilter(b_h, a_h, eeg_i, zi=zi_h)
    #
    #     eeg_i = eeg_i.reshape([1, 7500])
    #     acc_i = acc_i.reshape([1, 3, 750])
    #     data_handler = DataHandler()
    #     sleep_stage_res, wear_detect_res, cached_feature = data_handler.predict_with_single_epoch(eeg_i, acc_i, clf, cached_feature)
    #     sleep_stage_results.append(sleep_stage_res)
    #     # print("{}\t: sleep stage result:{}, wear detect result:".format(i, sleep_stage_res))
    # print(sleep_stage_results)