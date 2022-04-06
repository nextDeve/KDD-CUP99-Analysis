<template>
  <div :style="{ height: divHeight + 'px' }">
    <Upload
      action="/api/multiInput/"
      accept=".csv"
      name="multiInput"
      :show-upload-list="true"
      :on-success="upSuccess"
      :on-remove="removeList"
    >
      <Button icon="ios-cloud-upload-outline">上传文件</Button>
    </Upload>
    <Button
      type="primary"
      icon="ios-download"
      @click="downloadHeader"
      style="float: left"
    >
      导出所选特征
    </Button>

    <Button
      type="success"
      style="float: right"
      @click="startAnalyze"
      :loading="isLodding"
      :disabled="!this.$store.state.feature.isMultiAnalyzed"
    >
      <span v-if="!isLodding">开始分析</span>
      <span v-else>Loading...</span>
    </Button>
  </div>
</template>

<script>
import { Upload, ButtonGroup, Alert } from "view-design";
import { saveAs } from "file-saver";
export default {
  name: "MultiInput",
  data() {
    return {
      isError: false,
      isLodding: false,
      divHeight: 120,
    };
  },
  components: {
    Upload,
    ButtonGroup,
    Alert,
  },
  computed: {
    selectedFeature() {
      return this.$store.getters.selectedInfo;
    },
  },
  methods: {
    downloadHeader() {
      if (this.selectedFeature.length < 3) {
        this.$Message.error("请至少选择3钟特征！");
        return;
      }
      let res = [];
      this.selectedFeature.map((item) => {
        res.push(item.name);
      });

      let blob = new Blob([res.join(",")], {
        type: "text/plain;charset=utf-8",
      });
      saveAs(blob, "header.csv");
    },
    startAnalyze() {
      this.isLodding = true;
      this.$bus.$emit("showHotmap", "showMultiAnalyze");
    },
    upSuccess(response, file, fileList) {
      this.divHeight = 80 + fileList.length * 30;
      if (response.code === 200) {
        this.$Message.info("上传成功！");
        this.$store.commit("CHANGEMULTISTATE", true);
        this.$store.dispatch("saveMultiResponse", response);
      } else {
        this.$Message.error("上传失败！");
      }
    },
    removeList(file, fileList) {
      this.divHeight = 80 + fileList.length * 30;
    },
    changeAnalyzeState() {
      this.isLodding = false;
    },
  },
  mounted() {
    this.$bus.$on("changeMultiButtonState", this.changeAnalyzeState);
  },
};
</script>

<style>
</style>