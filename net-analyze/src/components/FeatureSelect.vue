<template>
  <div class="feature-select">
    <Row>
      <Col span="11">
        <Card style="width: 495px; height: 349px">
          <p slot="title">已选特征</p>
          <Scroll :height="260">
            <Tag
              type="dot"
              v-for="(feature, index) in constraintTerms"
              :key="index"
              closable
              color="primary"
              @on-close="handleRemoveFeature(index)"
              v-show="feature.selected"
              >{{ feature.name }}</Tag
            >
          </Scroll>
          <Button slot="extra" @click.prevent="changeAll(false)" type="warning"
            >清空</Button
          >
        </Card>
      </Col>
      <Col span="11" offset="2" style="margin-left: 46px">
        <Card style="width: 495px; height: 349px">
          <p slot="title">待选特征</p>
          <Scroll :height="260">
            <Tag
              type="border"
              style="height: 32px; line-height: 32px"
              v-for="(feature, index) in constraintTerms"
              :key="index"
              v-show="!feature.selected"
            >
              {{ feature.name }}
              <a href="" @click.prevent="handleAddFeature(index)">
                <Icon
                  type="ios-add"
                  size="20"
                  style="margin-left: 10px; color: red"
                />
              </a>
            </Tag>
          </Scroll>
          <Button slot="extra" @click.prevent="changeAll(true)" type="warning"
            >全选</Button
          >
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
import features from "@/assets/feature";
import { Scroll, Button, Card, Row, Col, Tag, Icon } from "view-design";
export default {
  name: "FeatureSelect",
  components: {
    Scroll,
    Button,
    Row,
    Col,
    Card,
    Tag,
    Icon,
  },
  data() {
    return {
      constraintTerms: features,
    };
  },
  watch: {
    constraintTerms: {
      handler(oldVal, newVal) {
        this.$store.dispatch("changeSelected", newVal);
      },
      deep: true,
    },
  },
  methods: {
    handleAddFeature(index) {
      this.constraintTerms[index].selected = true;
    },
    handleRemoveFeature(index) {
      this.constraintTerms[index].selected = false;
    },
    changeAll(state) {
      for (let index in this.constraintTerms) {
        this.constraintTerms[index].selected = state;
      }
    },
  },
};
</script>

<style scoped>
.feature-select {
  width: 1000px;
  height: 350px;
  margin: auto;
  margin-top: 10px;
  background-color: #ffffff;
  border: 1px solid rgb(241, 239, 239);
  box-shadow: 1px 2px 1px rgba(202, 191, 191, 0.1);
}
</style>