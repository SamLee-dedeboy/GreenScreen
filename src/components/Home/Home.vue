<script setup lang="ts">
import Card from '../Card/Card.vue'
import InputSearch from '../InputSearch/InputSearch.vue';
import recommend_channel from '../../assets/recommend_channel.json'
import { Ref, ref } from 'vue'
import * as vue from 'vue'

const carbon_emissions = ref(0)
const input_search = ref()
const visible = ref<boolean>(false);

const tree_num = vue.computed(() => {
    // return Array(Math.round(carbon_emissions.value/1000 / 0.072))
    return Array(Math.round(carbon_emissions.value/1000))
})

const showModal = () => {
      visible.value = true;
};
const handleOk = (e: MouseEvent) => {
      console.log(e);
      visible.value = false;
};

function handleSearchResult(result: any) {
    // carbon_emissions[result.title] = result.carbon_emission
    carbon_emissions.value = result.carbon
    console.log(result)
    showModal()
}

function handleCardClick(channel_url: string) {
    console.log(channel_url)
    input_search.value.search(channel_url)
}
</script>

<template>
    <div class="home-container">
        <InputSearch ref='input_search' @search_completed="handleSearchResult" />
        <div class="channels-container">
            <Card v-for="channel in recommend_channel"
                :channel="channel"
                @click="handleCardClick(channel.url)"
            />
        </div>
        <a-modal v-model:visible="visible" title="The carbon emission produced by the channel needs" @ok="handleOk">
            <span v-for="tree in tree_num"> 🌲 </span>
            <span> x1000,000 trees to compensate. </span>

        </a-modal>
    </div>
</template>

<style scoped>
@import "./Home.css"
</style>
