<template>
  <div class="site-wrapper">
    <header class="site-header">
      <div class="site-hearder-title">
        <img class="logo" alt="PeanutnWalnut logo" src="../assets/pnw_logo.jpg" width="200" />
        <h1>{{ title }}</h1>
        <h2>{{ subtitle }}</h2>
      </div>
    </header>
    <div class="content-wrapper">
      <div class="container">
        <!-- <Dropzone @dragenter="dragenter" @dragover="dragover" @dragleave="dragleave" @drop="drop" @click="click"
      @change="change" :is-dragged="isDragged" @remove="remove" :file-list="fileList" /> -->
        <Dropzone :is-dragged="isDragged" :file-list="fileList" @upload="startUpload" />
        <!-- <input type="submit" value="submit"> -->
      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Dropzone from './dropzone.vue'
import Footer from './footer.vue'

const title = ref('AI 자율주행 차선인식')
const subtitle = ref('( Autonomous-Driving-AI )')

let fileList = ref(null) as any
let isDragged = ref(false) as any

const dragenter = (status: boolean) => {
  isDragged.value = status
}
const dragover = (e: Event) => {
  e.preventDefault()
}
const dragleave = (status: boolean) => {
  isDragged.value = status
}
const drop = (e: DragEvent, status: boolean) => {
  e.preventDefault()
  isDragged.value = status
  const files = e.dataTransfer?.files
  addFiles(files)
}
const click = () => {
}
const change = (e: any) => {
  const files = e.target.files
  addFiles(files)
}
const remove = (idx: any) => {
  fileList.splice(idx, 1)
}

async function addFiles(files: any) {
  for (let i = 0; i < files.length; i++) {
    const src = await readFiles(files[i])
    files[i].src = src
    // fileList.push(files[i])
    console.log('addfile : ', i, files[i])
    console.log(src)
  }
}

async function readFiles(files: any) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = async (e: any) => {
      resolve(e.target.result)
    }
    reader.readAsDataURL(files)
  })
}

const startUpload = (files: File[]): void => {
  files.map(file => console.log("uploanding", file))
}

</script>

<style scss>
a {
  color: #42b983;
}

div {
  display: block;
  margin-bottom: 20px;
}

.content-wrapper {
  flex: 1 1;
}

.site-wapper {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}
</style>