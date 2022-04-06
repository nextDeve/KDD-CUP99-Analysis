<template>
  <Card
    style="width: 1000px; height: 700px; margin-top: 10px; margin-bottom: 50px"
  >
    <p slot="title">分析结果</p>
    <Alert show-icon v-show="isNodata">
      提示信息
      <template slot="desc">暂无分析数据 </template>
    </Alert>
    <p v-show="this.$store.state.feature.isSingleAnalyzed">
      本次预测结果为：{{ singlePredictType }}
    </p>
    <div
      v-show="this.$store.state.feature.isSingleAnalyzed"
      ref="showSingleAnalyze"
      style="width: 1000px; height: 600px"
    ></div>

    <div v-show="this.$store.state.feature.isMultiAnalyzed">
      <p>共上传{{ this.$store.state.feature.multiPredict.length }}条数据</p>
      <div
        v-show="this.$store.state.feature.isMultiAnalyzed"
        ref="showMultiAnalyze"
        style="width: 1000px; height: 600px; margin: auto"
      ></div>
    </div>

    <Button
      :type="showType === 1 ? 'primary' : 'default'"
      slot="extra"
      style="margin-right: 10px"
      @click.prevent="showHotmap(hotMapType)"
    >
      特征系数热力图
    </Button>
    <Button
      :type="showType === 2 ? 'primary' : 'default'"
      slot="extra"
      @click.prevent="showrResult"
    >
      网络攻击预测
    </Button>
  </Card>
</template>

<script>
import { Card, Alert } from "view-design";
import * as echarts from "echarts/core";
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  LegendComponent,
} from "echarts/components";
import { HeatmapChart, BarChart, PieChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";
import { LabelLayout } from "echarts/features";
echarts.use([
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  HeatmapChart,
  BarChart,
  CanvasRenderer,
  TitleComponent,
  LegendComponent,
  PieChart,
  LabelLayout,
]);
export default {
  components: {
    Card,
    Alert,
  },
  data() {
    return {
      showType: 1,
    };
  },
  computed: {
    isNodata() {
      let isS = this.$store.state.feature.isMultiAnalyzed;
      let isM = this.$store.state.feature.isSingleAnalyzed;
      if (isS || isM) return false;
      else return true;
    },
    cofHotmapData() {
      let data = this.$store.state.feature.cof;
      let min = Infinity;
      let max = -Infinity;
      data.forEach((item) => {
        if (item[2] > max) max = item[2];
        if (item[2] < min) min = item[2];
      });
      return {
        data,
        min,
        max,
      };
    },
    HotmapOption() {
      return {
        tooltip: {
          position: "top",
        },
        grid: {
          height: `${this.$store.state.feature.features.length * 2.2}%`,
          top: "0%",
        },
        xAxis: {
          type: "category",
          name: "类别",
          data: this.$store.state.feature.label,
          show: true,
          axisLabel: {
            interval: 0,
            rotate: "270",
            fontFamily: "Microsoft YaHei",
            fontSize: 10,
          },
        },
        yAxis: {
          type: "category",
          name: "特征",
          data: this.$store.state.feature.features,
          show: true,
          axisLabel: {
            interval: 0,
            fontSize: 10,
          },
        },
        visualMap: {
          type: "piecewise",
          min: this.cofHotmapData.min,
          max: this.cofHotmapData.max,
          calculable: true,
          orient: "horizontal",
          splitNumber: 10,
          show: false,
        },
        series: [
          {
            name: "特征系数热力图",
            type: "heatmap",
            data: this.cofHotmapData.data,
            label: {
              show: true,
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };
    },
    singleProbOption() {
      return {
        grid: {
          height: `80%`,
          top: "10%",
        },
        xAxis: {
          type: "category",
          name: "类别",
          data: this.$store.state.feature.label,
          axisLabel: {
            interval: 0,
            rotate: "270",
            fontFamily: "Microsoft YaHei",
          },
        },
        yAxis: {
          type: "value",
          name: "概率",
        },
        series: [
          {
            name: "预测概率直方图",
            data: this.$store.state.feature.singlePredictProb,
            type: "bar",
          },
        ],
      };
    },
    singlePredictType() {
      let predict = this.$store.state.feature.singlePredict;
      if (predict === -1) return "";
      return this.$store.state.feature.labelMap[predict];
    },
    hotMapType() {
      if (this.$store.state.feature.isSingleAnalyzed)
        return "showSingleAnalyze";
      if (this.$store.state.feature.isMultiAnalyzed) return "showMultiAnalyze";
      return "showSingleAnalyze";
    },
    multiPredictOption() {
      let legendData = [];
      let seriesData = [];
      let allPredict = [];
      this.$store.state.feature.multiPredict.forEach((item) => {
        let label = this.$store.state.feature.labelMap[item];
        allPredict.push(label);
        if (legendData.indexOf(label) == -1) {
          legendData.push(label);
          seriesData.push({ name: label, value: 0 });
        }
      });
      allPredict.forEach((item) => {
        let index = legendData.indexOf(item);
        seriesData[index].value += 1;
      });
      return {
        title: {
          text: "批量分析预测统计",
          left: "center",
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend: {
          type: "scroll",
          orient: "vertical",
          right: 100,
          top: 20,
          bottom: 20,
          data: legendData,
        },
        series: [
          {
            name: "预测次数统计",
            type: "pie",
            radius: "55%",
            center: ["40%", "50%"],
            data: seriesData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };
    },
  },
  methods: {
    showHotmap(showRef = "showSingleAnalyze") {
      //有的话就获取已有echarts实例的DOM节点。
      let myChart = echarts.getInstanceByDom(this.$refs[showRef]);
      if (myChart == null) {
        // 如果不存在，就进行初始化
        myChart = echarts.init(this.$refs[showRef]);
      }
      myChart.setOption(this.HotmapOption, true);
      this.showType = 1;
      if (showRef == "showMultiAnalyze") {
        this.$bus.$emit("changeMultiButtonState");
      }
    },
    showrResult() {
      this.showType = 2;
      if (this.$store.state.feature.isSingleAnalyzed) {
        let chartDom = this.$refs.showSingleAnalyze;
        let myChart = echarts.init(chartDom);
        myChart.setOption(this.singleProbOption, true);
      } else if (this.$store.state.feature.isMultiAnalyzed) {
        let chartDom = this.$refs.showMultiAnalyze;
        var myChart = echarts.init(chartDom);
        myChart.setOption(this.multiPredictOption, true);
      }
    },
  },
  mounted() {
    this.$bus.$on("showHotmap", this.showHotmap);
  },
  destroyed() {
    this.$bus.$off("showHotmap");
  },
};
</script>

<style>
</style>