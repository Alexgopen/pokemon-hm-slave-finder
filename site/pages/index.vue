<template>
  <section class="container">
    <h1>Pokemon Move Finder Thing</h1>

    <div class="block">
      <h2>Which generation are you playing?</h2>
      <select v-model="generationSelection" @change="generationChanged($event)">
        <option v-for="g in generations" v-bind:value="g">
          {{g.text}}
        </option>
      </select>
    </div>

    <div v-if="generationSelection" class="block">
      <h2>Which moves do you need the Pokemon to know?</h2>
      <ul>
        <li v-for="hm in hms">
          <input type="checkbox" :id="hm.name" :value="hm.name" v-model="hmSelection" @change="hmChanged">
          <label :for="hm">{{hm.name}}</label>
        </li>
      </ul>
    </div>

    <div v-if="hmSelection.length > 0" class="block">
      <h2 v-if="pokemon.length > 0">These Pokemon can learn those moves:</h2>
      <h2 v-else>No Pokemon can learn those moves.</h2>
      <div class="flex-container">
        <pokemon v-for="p in pokemon" :pokemon="p" :generation="generationSelection.dir" :serebiiGenerationSuffix="generationSelection.suffix"/>
      </div>
    </div>
  </section>
</template>

<script>
import intersectionBy from 'lodash'

import Pokemon from '~/components/Pokemon.vue'
import json from '~/static/hm_data.json'

export default {
  components: {
    Pokemon
  },

  data() {
    return {
      checkedNames: [],
      pokemon: [],
      generations: [
        {text: "Red/Blue/Yellow", dir: "gen1", suffix: ""},
        {text: "Gold/Silver/Crystal", dir: "gen2", suffix: "-gs"},
        {text: "Ruby/Sapphire/Emerald/FireRed/LeafGreen", dir: "gen3", suffix: "-rs"},
        {text: "Diamond/Pearl/Platinum/SoulSilver/HeartGold", dir: "gen4", suffix: "-dp"}
      ],
      generationSelection: null,
      hms: [],
      hmSelection: [],
    }
  },

  methods: {
    clearPokemon: function(event) {
      this.pokemon.splice(0, this.pokemon.length);
    },

    hmChanged: function(event) {
      this.updatePokemonList();
    },

    generationChanged: function(event) {
      this.updateHmList();
      this.updatePokemonList();
    },

    updateHmList: function(event) {
      this.hms.splice(0, this.hms.length);

      var k = Object.keys(json[this.generationSelection.dir])

      k.forEach((e) => {
        this.hms.push({name: e});
      });

      this.hmSelection = [];
    },

    updatePokemonList: function(event) {
      this.clearPokemon();

      if (this.generationSelection === null || this.hmSelection == null) {
        return;
      }

      var hmPokemon = [];

      this.hmSelection.forEach((hm) => {
        if (hmPokemon.length == 0) {
          hmPokemon = json[this.generationSelection.dir][hm];
        }
        else {
          hmPokemon = _.intersectionBy(hmPokemon, json[this.generationSelection.dir][hm], 'id');
        }
      });

      hmPokemon.forEach((e) => {
        this.pokemon.push(e);
      });
    }
  }
};
</script>

<style>
.block {
  margin-top: 5%;
  padding: 5%;
  border: 1px solid #5c5c5c;
}

select {
  width: 100%;
}

ul {
  list-style: none;
}

.flex-container {
  display: flex;
  flex-wrap: wrap;
}

h2 {
  margin-bottom: 5%;
}

html {
    overflow: -moz-scrollbars-vertical; 
    overflow-y: scroll;
    height: 200%
}
</style>
