<template>
  <div class="feature-input">
    <Card style="width: 100%; height: 100%">
      <p slot="title">特征输入</p>
      <SingleInput v-if="inputType === 1"></SingleInput>
      <MultiInput v-if="inputType === 2"></MultiInput>
      <Button
        :type="inputType === 1 ? 'primary' : 'default'"
        slot="extra"
        @click.prevent="changeInputType(1)"
      >
        单个分析
      </Button>
      <Button
        :type="inputType === 2 ? 'primary' : 'default'"
        style="margin-left: 10px"
        slot="extra"
        @click.prevent="changeInputType(2)"
      >
        批量分析
      </Button>
    </Card>
  </div>
</template>

<script>
import SingleInput from "./SingleInput/index.vue";
import MultiInput from "./MultiInput/index.vue";
import { Card, Icon, ButtonGroup } from "view-design";
export default {
  name: "FeatureInput",
  components: {
    SingleInput,
    MultiInput,
    Card,
    Icon,
    ButtonGroup,
  },
  data() {
    return {
      inputType: 1,
    };
  },
  computed: {
    selectedFeature() {
      return this.$store.getters.selectedInfo;
    },
  },
  methods: {
    changeInputType(type) {
      this.inputType = type;
      if (type == 1) {
        //doSomething
      } else {
        //doSomething
      }
    },
  },
};
</script>

<style scoped>
.feature-input {
  width: 1000px;
  margin: auto;
  margin-top: 10px;
  background-color: #ffffff;
  border: 1px solid rgb(241, 239, 239);
  box-shadow: 1px 2px 1px rgba(202, 191, 191, 0.1);
}
</style>