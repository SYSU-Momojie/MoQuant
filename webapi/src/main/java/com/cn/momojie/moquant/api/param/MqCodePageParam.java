package com.cn.momojie.moquant.api.param;

import lombok.Data;

@Data
public class MqCodePageParam {

	private String tsCode;

	private Integer pageNum = 1;

	private Integer pageSize = 20;
}
