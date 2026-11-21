<script setup>

</script>

<template>
  <div class="page text-center">


      <div class="video-wrapper">
        <iframe
          src="https://player.bilibili.com/player.html?isOutside=true&aid=115671186867538&bvid=BV14b2sBYE2U&cid=34545270848&p=3"
          scrolling="no"
          frameborder="0"
          allowfullscreen
        ></iframe>
      </div>
  </div>
</template>

<style scoped>
.video-wrapper {
  width: 100%;
  max-width: 960px;   /* 可选：限制最大宽度 */
  margin: 0 auto;     /* 居中 */
  aspect-ratio: 16 / 9;
}

.video-wrapper iframe {
  width: 100%;
  height: 100%;
  border: none;
}
</style>