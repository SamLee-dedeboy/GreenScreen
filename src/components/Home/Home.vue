<script setup lang="ts">
import Card from '../Card/Card.vue'
import InputSearch from '../InputSearch/InputSearch.vue';
import recommend_channel from '../../assets/recommend_channel.json'
import { Ref, ref } from 'vue'

const carbon_emissions = ref({})
const input_search = ref()
function handleSearchResult(result: any) {
    carbon_emissions[result.title] = result.carbon_emission
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
                :carbon_emission="carbon_emissions[channel.title]"
            />
        </div>
    </div>
</template>

<style scoped>
@import "./Home.css"
</style>
