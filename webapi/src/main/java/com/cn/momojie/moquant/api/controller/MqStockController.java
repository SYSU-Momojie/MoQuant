package com.cn.momojie.moquant.api.controller;

import com.cn.momojie.moquant.api.param.MqCodePageParam;
import com.cn.momojie.moquant.api.param.MqDailyBasicParam;
import com.cn.momojie.moquant.api.param.MqMessageParam;
import com.cn.momojie.moquant.api.param.MqShareListParam;
import com.cn.momojie.moquant.api.param.MqTrendParam;
import com.cn.momojie.moquant.api.service.MqInfoQueryService;
import com.cn.momojie.moquant.api.vo.MqForecastInfo;
import com.cn.momojie.moquant.api.vo.MqShareDetail;
import com.cn.momojie.moquant.api.vo.MqShareTrend;
import com.cn.momojie.moquant.api.vo.PageResult;
import com.cn.momojie.moquant.api.vo.ShareListItem;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class MqStockController {

    @Autowired
    private MqInfoQueryService mqInfoQueryService;

    @RequestMapping(path = "getPageList", method = RequestMethod.POST)
    public PageResult getPageList(@RequestBody MqDailyBasicParam param) {
        return mqInfoQueryService.getLatestListByOrder(param);
    }

    @RequestMapping(path = "getGrowList", method = RequestMethod.POST)
    public PageResult getGrowList(@RequestBody MqShareListParam param) {
        return mqInfoQueryService.getGrowList(param);
    }

    @RequestMapping(path = "getValList", method = RequestMethod.POST)
    public PageResult getValList(@RequestBody MqShareListParam param) {
        return mqInfoQueryService.getValList(param);
    }

    @RequestMapping(path = "getLatestByCode", method = RequestMethod.POST)
    public MqShareDetail getLatestByCode(@RequestBody String tsCode) {
        return mqInfoQueryService.getLatestByCode(tsCode);
    }

    @RequestMapping(path = "getTrendByCode", method = RequestMethod.POST)
    public MqShareTrend getTrendByCode(@RequestBody MqTrendParam param) {
        return mqInfoQueryService.getTrend(param);
    }

    @RequestMapping(path = "getAllShareForSearch", method = RequestMethod.POST)
    public List<ShareListItem> getAllShareForSearch() {
        return mqInfoQueryService.getAllShare();
    }

    @RequestMapping(path = "getNoteList", method = RequestMethod.POST)
    public PageResult getNoteList(@RequestBody MqCodePageParam param) {
        return mqInfoQueryService.getNotes(param);
    }

	@RequestMapping(path = "getForecastInfo", method = RequestMethod.POST)
	public MqForecastInfo getForecastInfo(@RequestBody String tsCode) {
		return mqInfoQueryService.getForecastInfo(tsCode);
	}

	@RequestMapping(path = "getLatestReportList", method = RequestMethod.POST)
	public PageResult getLatestReportList(@RequestBody MqMessageParam param) {
    	return mqInfoQueryService.getLatestReportList(param);
	}
}
