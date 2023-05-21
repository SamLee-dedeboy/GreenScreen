<script setup lang="ts">
import { Ref, ref } from "vue"
import * as vue from 'vue'
import * as d3 from 'd3'
import scroller from "./scroller"
import slides from '../../assets/SlideShow/slides.html?raw'

vue.onMounted(() => {
    setupScroller()
})

function setupScroller() {
    // setup scroll functionality
    let scroll: any = scroller.scroller()
        .container(d3.select('.slide-container'));

    // pass in .section selection as the sections
    scroll(d3.selectAll('.section'));

    // setup event handling
    d3.selectAll('.section').each(function (this: any) {
        console.log(this)
        // general section transition
        remove_general_highlight(this)
    })
    scroll.on('active', function (index) {
        // remove previous highlights

        // highlight vis
        apply_general_highlight(index)
        
        // TODO: define section-specific transitions

    });

    scroll.on('progress', function (index, progress) {

    });
}

function apply_general_highlight(index: number) {
    const active_section = d3.select(`.slide${index+1}`)
    console.log(active_section.node())
    active_section.select('.header').style("opacity", 1)
    active_section.select('.content').style("opacity", 1)
    active_section.selectAll("img").style("opacity", 0.6)    
}

function remove_general_highlight(element: any) {
    console.log(d3.select(element).node())
    d3.select(element).select('.header').style("opacity", 0.1)
    d3.select(element).select('.content').style("opacity", 0.1)
    d3.select(element).selectAll('img').style("opacity", 0.1)
}

</script>

<template>
    <div class="slideshow-container" v-html="slides">
    </div>

</template>

<style scoped>
@import './SlideShow.css'
</style>