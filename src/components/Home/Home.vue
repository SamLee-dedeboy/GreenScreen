<script setup lang="ts">
import Card from '../Card/Card.vue'
import InputSearch from '../InputSearch/InputSearch.vue';
import recommend_channel from '../../assets/recommend_channel.json'
import { Ref, ref } from 'vue'



function handleSearchResult(result: any) {
    console.log(result)
}
</script>

<template>
    <InputSearch @search_completed="handleSearchResult" />
    <div class="channels-container">
        <Card v-for="channel in recommend_channel"
            :channel="channel"
        />
    </div>
</template>

<style scoped>
@import "./Home.css"
</style>
