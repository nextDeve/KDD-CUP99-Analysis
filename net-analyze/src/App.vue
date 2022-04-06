<template>
  <div class="main-containers">
    <Header />
    <FeatureSelect />
    <FeatureInput />
    <ShowResult />
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import FeatureSelect from "@/components/FeatureSelect.vue";
import FeatureInput from "@/components/FeatureInput/index.vue";
import ShowResult from "@/components/ShowResult.vue";
export default {
  name: "App",
  components: { Header, FeatureSelect, FeatureInput, ShowResult },
};
</script>

<style scoped lang='css'>
body {
  background-color: #f8f8ff;
}

.main-containers {
  position: relative;
  top: 10px;
  width: 1000px;
  margin: auto;
  background-color: #ffffff;
}
</style>
