<script setup lang="ts">
import * as vue from 'vue'
import * as numeral from 'numeral'
import { Ref, ref } from 'vue'

const props = defineProps({
  channel: {
    type: Object,
    required: true
  },
  carbon_emission: {
    type: Number,
  }
})

console.log(props.channel)

</script>

<template>
    <div v-if="channel" class='channel-card' >
        <div class="channel-card-header">
            <img class="channel-image" :src="'public/channel_images/' + channel.title + '.jpg'" />
        </div>
        <div class="channel-card-content">
            <span class="card-title"> {{ channel.title }} </span>
            <p class="card-content"> 
                <span class="content-item-header"> Subs:  </span> 
                {{ numeral(channel.subs).format('0,0') }} 
            </p>
            <p class="card-content">
                <span class="content-item-header">  Videos:  </span> 
                {{ channel.videos }} 
            </p>
            <p class="card-content"> 
                <span class="content-item-header">  CEs:  </span> 
                {{ carbon_emission || "Click to find out" }} 
                </p>
            </div>
        </div>
</template>

<style scoped>
@import "./Card.css"

</style>
