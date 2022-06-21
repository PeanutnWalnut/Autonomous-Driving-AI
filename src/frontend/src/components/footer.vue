<template>
  <footer>
    <div class='container'>
      <div class='footer-content'>
        <ul id='footer_menu' class='list-unstyled'>
          <li class='inline'>
            <span class='footer-content-madeby'>Made by</span>
            <a class='footer-content-link' href='/'>PeanutnWalnut</a>
          </li>
        </ul>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
</script>

<style lang="scss">
.footer-content {
  border-top: 2px solid #efefefef;
  height: 60px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  text-align: center;
}
.footer-content-link {
  margin-left: 9px;
  text-decoration: none;
  color: #42b983;
}
.list-unstyled {
  padding: 0;
  list-style: none;
}
.container {
  padding: 0 60px;
  margin: 0 auto;
  max-width: 1400px;
}
</style>