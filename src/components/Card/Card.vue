<script setup lang="ts">
import * as vue from 'vue'
import { Ref, ref } from 'vue'

const props = defineProps({
  channel: {
    type: Object,
    required: true
  }
})

console.log(props.channel)

</script>

<template>
    <a-card v-if="channel" class='channel-card' title="Card title" :bordered="false" >
      <p class="card-content1"> {{ channel.subs }} </p>
      <p class="card-content2"> {{ channel.videos }} </p>
      <p class="card-content3"> {{ channel.carbon_emission }} </p>
    </a-card>
</template>

<style scoped>
@import "./Card.css"

</style>
