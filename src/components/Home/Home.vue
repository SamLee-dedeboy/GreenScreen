<script setup lang="ts">
import Card from '../Card/Card.vue'
import InputSearch from '../InputSearch/InputSearch.vue';
import recommend_channel from '../../assets/recommend_channel.json'
import { Ref, ref } from 'vue'


const server_address = 'localhost:5173'
async function handleSearchResult(channel_url: any) {
    await fetch(`${server_address}/channel/${channel_url}`)
        .then(res => res.json())
        .then(json => {
            console.log("channel data fetched", json)
        })
}
</script>

<template>
    <div class="home-container">
        <InputSearch @search_completed="handleSearchResult" />
        <div class="channels-container">
            <Card v-for="channel in recommend_channel"
                :channel="channel"
            />
        </div>
    </div>
</template>

<style scoped>
@import "./Home.css"
</style>
