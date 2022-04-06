<template>
  <div style="min-height: 40px">
    <Form :inline="true" label-position="top">
      <Row>
        <Col span="8">
          <div v-for="x in totalRow" :key="x">
            <FormItem
              :label="selectedFeature[(x - 1) * 3].name"
              v-if="
                (x - 1) * 3 < selectedFeature.length &&
                !symbolFeature.hasOwnProperty(selectedFeature[(x - 1) * 3].name)
              "
            >
              <InputNumber
                style="width: 190px"
                v-model="feature[selectedFeature[(x - 1) * 3].name]"
              ></InputNumber>
            </FormItem>
            <FormItem
              v-if="
                (x - 1) * 3 < selectedFeature.length &&
                symbolFeature.hasOwnProperty(selectedFeature[(x - 1) * 3].name)
              "
              :label="selectedFeature[(x - 1) * 3].name"
            >
              <Select
                style="width: 190px"
                v-model="feature[selectedFeature[(x - 1) * 3].name]"
              >
                <Option
                  v-for="(item, index) in symbolFeature[
                    selectedFeature[(x - 1) * 3].name
                  ]"
                  :value="item"
                  :key="index"
                  >{{ item }}</Option
                >
              </Select>
            </FormItem>
          </div>
        </Col>
        <Col span="8">
          <div v-for="x in totalRow" :key="x">
            <FormItem
              :label="selectedFeature[(x - 1) * 3 + 1].name"
              v-if="
                (x - 1) * 3 + 1 < selectedFeature.length &&
                !symbolFeature.hasOwnProperty(
                  selectedFeature[(x - 1) * 3 + 1].name
                )
              "
            >
              <InputNumber
                style="width: 190px"
                v-model="feature[selectedFeature[(x - 1) * 3 + 1].name]"
              ></InputNumber>
            </FormItem>
            <FormItem
              v-if="
                (x - 1) * 3 + 1 < selectedFeature.length &&
                symbolFeature.hasOwnProperty(
                  selectedFeature[(x - 1) * 3 + 1].name
                )
              "
              :label="selectedFeature[(x - 1) * 3 + 1].name"
            >
              <Select
                style="width: 190px"
                v-model="feature[selectedFeature[(x - 1) * 3 + 1].name]"
              >
                <Option
                  v-for="(item, index) in symbolFeature[
                    selectedFeature[(x - 1) * 3 + 1].name
                  ]"
                  :value="item"
                  :key="index"
                  >{{ item }}</Option
                >
              </Select>
            </FormItem>
          </div>
        </Col>
        <Col span="8">
          <div v-for="x in totalRow" :key="x">
            <FormItem
              :label="selectedFeature[(x - 1) * 3 + 2].name"
              v-if="
                (x - 1) * 3 + 2 < selectedFeature.length &&
                !symbolFeature.hasOwnProperty(
                  selectedFeature[(x - 1) * 3 + 2].name
                )
              "
            >
              <InputNumber
                style="width: 190px"
                v-model="feature[selectedFeature[(x - 1) * 3 + 2].name]"
              ></InputNumber>
            </FormItem>
            <FormItem
              v-if="
                (x - 1) * 3 + 2 < selectedFeature.length &&
                symbolFeature.hasOwnProperty(
                  selectedFeature[(x - 1) * 3 + 2].name
                )
              "
              :label="selectedFeature[(x - 1) * 3 + 2].name"
            >
              <Select
                style="width: 190px"
                v-model="feature[selectedFeature[(x - 1) * 3 + 2].name]"
              >
                <Option
                  v-for="(item, index) in symbolFeature[
                    selectedFeature[(x - 1) * 3 + 2].name
                  ]"
                  :value="item"
                  :key="index"
                  >{{ item }}</Option
                >
              </Select>
            </FormItem>
          </div>
        </Col>
      </Row>
      <Button
        type="success"
        @click="startAnalyze"
        :loading="isLodding"
        style="position: relative; left: 850px"
      >
        <span v-if="!isLodding">开始分析</span>
        <span v-else>Loading...</span>
      </Button>
    </Form>
  </div>
</template>

<script>
import {
  Form,
  FormItem,
  InputNumber,
  Row,
  Col,
  Option,
  Select,
} from "view-design";
import { reqAnalyze } from "@/api/index.js";
export default {
  name: "SingleInput",
  components: {
    Form,
    FormItem,
    InputNumber,
    Row,
    Col,
    Option,
    Select,
  },
  data() {
    return {
      isLodding: false,
      feature: {
        duration: 0,
        protocol_type: "",
        service: "",
        flag: "",
        src_bytes: 0,
        dst_bytes: 0,
        land: 0,
        wrong_fragment: 0,
        urgent: 0,
        hot: 0,
        num_failed_logins: 0,
        logged_in: 0,
        num_compromised: 0,
        root_shell: 0,
        su_attempted: 0,
        num_root: 0,
        num_file_creations: 0,
        num_shells: 0,
        num_access_files: 0,
        num_outbound_cmds: 0,
        is_host_login: 0,
        is_guest_login: 0,
        count: 0,
        srv_count: 0,
        serror_rate: 0,
        srv_serror_rate: 0,
        rerror_rate: 0,
        srv_rerror_rate: 0,
        same_srv_rate: 0,
        diff_srv_rate: 0,
        srv_diff_host_rate: 0,
        dst_host_count: 0,
        dst_host_srv_count: 0,
        dst_host_same_srv_rate: 0,
        dst_host_diff_srv_rate: 0,
        dst_host_same_src_port_rate: 0,
        dst_host_srv_diff_host_rate: 0,
        dst_host_serror_rate: 0,
        dst_host_srv_serror_rate: 0,
        dst_host_rerror_rate: 0,
        dst_host_srv_rerror_rate: 0,
      },
    };
  },
  computed: {
    selectedFeature() {
      return this.$store.getters.selectedInfo;
    },
    totalRow() {
      return Math.ceil(this.selectedFeature.length / 3);
    },
    symbolFeature() {
      return this.$store.state.feature.featureMap;
    },
    selectedFeatureName() {
      let features = [];
      this.$store.getters.selectedInfo.forEach((element) => {
        features.push(element.name);
      });
      return features;
    },
  },
  watch: {
    selectedFeature: {
      handler() {
        this.feature = {
          duration: 0,
          protocol_type: "",
          service: "",
          flag: "",
          src_bytes: 0,
          dst_bytes: 0,
          land: 0,
          wrong_fragment: 0,
          urgent: 0,
          hot: 0,
          num_failed_logins: 0,
          logged_in: 0,
          num_compromised: 0,
          root_shell: 0,
          su_attempted: 0,
          num_root: 0,
          num_file_creations: 0,
          num_shells: 0,
          num_access_files: 0,
          num_outbound_cmds: 0,
          is_host_login: 0,
          is_guest_login: 0,
          count: 0,
          srv_count: 0,
          serror_rate: 0,
          srv_serror_rate: 0,
          rerror_rate: 0,
          srv_rerror_rate: 0,
          same_srv_rate: 0,
          diff_srv_rate: 0,
          srv_diff_host_rate: 0,
          dst_host_count: 0,
          dst_host_srv_count: 0,
          dst_host_same_srv_rate: 0,
          dst_host_diff_srv_rate: 0,
          dst_host_same_src_port_rate: 0,
          dst_host_srv_diff_host_rate: 0,
          dst_host_serror_rate: 0,
          dst_host_srv_serror_rate: 0,
          dst_host_rerror_rate: 0,
          dst_host_srv_rerror_rate: 0,
        };
      },
      deep: true,
    },
  },
  methods: {
    startAnalyze() {
      if (this.selectedFeature.length < 3) {
        this.$Message.error("请至少选择3钟特征！");
        return;
      }
      this.isLodding = true;
      reqAnalyze({
        featureName: this.selectedFeatureName,
        values: this.feature,
      }).then(
        (response) => {
          this.isLodding = false;
          this.$store.commit("CHANGESINGLESTATE", true);
          this.$store.dispatch("saveSingelResponse", response.data);
          this.$bus.$emit("showHotmap");
        },
        () => {
          this.isLodding = false;
        }
      );
    },
  },
};
</script>

<style>
</style>