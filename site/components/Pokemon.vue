<template>
  <div class="pokemon">
    <img :src="`img/${generation}/${pokemon.id}.png`">

    <span>
      <a :href="`https://www.serebii.net/pokedex${serebiiGenerationSuffix}/${pokemon.id}.shtml`">{{pokemon.name}}</a>
    </span>
  </div>
</template>

<script>
export default {
  props: ["pokemon", "generation", "serebiiGenerationSuffix"]
}
</script>

<style>

a {
  color: white;
}

.pokemon {
  border: 1px #373737 solid;
  flex: 0 0 50%;
}

.pokemon > img {
  width: 20%;
  height: auto;
  vertical-align: middle;
}
</style>
