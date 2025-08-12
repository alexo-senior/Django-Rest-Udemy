<script setup>
import encabezado from '@/components/icons/encabezado.vue';
import Footer from './Footer.vue';
</script>

<template>
  <encabezado />

  <div
    class="breadcumb-area bg-img bg-overlay"
    style="background-image: url(img/bg-img/breadcumb3.jpg)"
  >
    <div class="container h-100">
      <div class="row h-100 align-items-center">
        <div class="col-12">
          <div class="breadcumb-text text-center">
            <h2>Recetas flaites - Desarrollado con Vue 3</h2>
          </div>
        </div>
      </div>
    </div>
  </div>

  <section class="top-catagory-area section-padding-80-0">
    <div class="container"></div>
  </section>
  <section class="best-receipe-area">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <div class="section-heading">
            <h3>Últimas recetas publicadas</h3>
          </div>
        </div>
      </div>

      <div class="row"></div>
    </div>
  </section>
  <Footer />
</template>

<style scoped></style>
