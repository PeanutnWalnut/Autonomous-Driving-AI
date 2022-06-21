<template>
  <div class="wrapper">
    <!-- <div class="file-upload-container" @dragenter="onDragenter" @dragover="onDragover" @dragleave="onDragleave"
      @drop="onDrop" @click="onClick"> -->
    <div class="file-upload-container" @drop.prevent="handleDrop" @dragenter="isdragged=true" @drageleave="isdragged=false" @dragover="handleDragover">
      <!-- <div class="file-upload" :class="props.isDragged ? 'dragged' : ''"> -->
      <div class="file-upload" :class="isdragged ? 'dragged' : ''">
        Drag & Drop Files
      </div>
    </div>

    <!-- file uploade -->
    <!-- <input type="file" ref="fileInput" class="file-upload-input" @change="onFileChange" multiple> -->
    <input type="file" ref="fileInput" class="file-upload-input" @input="handleInput" multiple>

    <!-- upload file-list -->
    <div class="file-upload-list">
      <div class="file-upload-list__item" v-for="(file, index) in fileList" :key="index">
        <div class="file-upload-list__item__data">
          <img class="file-upload-list__item__data-thumbnail" :src="file.src">
          <div class="file-upload-list__item__data-name">
            {{ file.name }}
          </div>
        </div>
        <!-- <div class="file-upload-list__item__btn-remove" @click="handleRemove(index)">
          delete
        </div> -->
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

const events = ["dragenter", "dragover", "dragleave", "drop", "click", "change", "remove"]
onMounted(() => { events.forEach(event => document.body.addEventListener(event, (e) => e.preventDefault())) })
onUnmounted(() => { events.forEach(event => document.body.removeEventListener(event, (e) => e.preventDefault())) })

interface props {
  isDragged?: boolean
  fileList?: any
}

const props = withDefaults(defineProps<props>(), {
  isDragged: false
})

// const eimts = defineEmits(["dragenter", "dragover", "dragleave", "drop", "click", "change", "remove"])
// const onClick = () => { eimts("click") }
// const onDragenter = () => { eimts("dragenter", true) }
// const onDragover = (e: Event) => { eimts("dragover", e) }
// const onDragleave = () => { eimts("dragleave", false) }
// const onFileChange = () => { eimts("change") }
// const onDrop = (e: any) => { eimts("drop", e, false) }
// const handleRemove = (idx: any) => { eimts("remove", idx) }

const isdragged = ref(false)

const eimts=defineEmits<{(e:"upload",files:File[]):void}>()

const handleDrop = (e:DragEvent):void=>{
  isdragged.value=false
  const files = e.dataTransfer?.files as FileList | null
  eimts("upload", [...files])
}

const handleInput = (e:InputEvent):void=>{
  const files = (e.target as HTMLInputElement).files as FileList
  eimts("upload", [...files])
}

const handleDragover = (e:DragEvent):void=>{e.preventDefault()}
</script>

<style lang="scss">
.container {
  min-height: 300px;
  width: 500px;
  max-width: 1400px;
  margin: 0 auto;
}
.file-upload {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  border: transparent;
  border-radius: 20px;
  cursor: pointer;
  &.dragged {
    border: 1px dashed powderblue;
    opacity: .6;
  }
  &-container {
    height: 300px;
    width: 400px;
    padding: 20px;
    margin: 0 auto;
    box-shadow: 0 0.625rem 1.25rem #0000001a;
    border-radius: 20px;
  }
  &-input {
    display: none;
  }
  &-list {
    margin-top: 10px;
    width: 100%;
    &__item {
      padding: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      &__data {
        display: flex;
        align-items: center;
        &-thumbnail {
          margin-right: 10px;
          border-radius: 20px;
          width: 120px;
          height: 120px;
        }
      }
      &__btn-remove {
        cursor: pointer;
        border: 1px solid powderblue;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 5px;
        border-radius: 6px;
      }
    }
  }
}
input {
  cursor: pointer;
  border: 1px solid powderblue;
  justify-content: center;
  align-items: center;
  padding: 5px;
  border-radius: 6px;
  background-color: transparent;
}
</style>
