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
      
      <table>
        <tr>
          <th>HM</th>
          <th>TM / Learned</th>
        </tr>
        <tr>
          <td>
            <ul>
              <li v-for="hm in hms">
                <input type="checkbox" :id="hm.name" :value="hm.name" v-model="hmSelection" @change="movesChanged">
                <label :for="hm">{{hm.name}}</label>
              </li>
            </ul>
          </td>
          <td>
            <ul>
              <li v-for="tm in tms">
                <input type="checkbox" :id="tm.name" :value="tm.name" v-model="tmSelection" @change="movesChanged">
                <label :for="tm">{{tm.name}}</label>
              </li>
            </ul>
          </td>
        </tr>
      </table>
    </div>

    <div v-if="moveSelection.length > 0" class="block">
      <h2 v-if="pokemon.length > 0">These Pokemon can learn those moves:</h2>
      <h2 v-else>No Pokemon can learn those moves.</h2>
      <div class="flex-container">
        <pokemon v-for="p in pokemon" :pokemon="p" :generation="generationSelection.gen" :serebiiGenerationSuffix="generationSelection.suffix"/>
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
        {text: "Red/Blue/Yellow", gen: "gen1", suffix: ""},
        {text: "Gold/Silver/Crystal", gen: "gen2", suffix: "-gs"},
        {text: "Ruby/Sapphire/Emerald/FireRed/LeafGreen", gen: "gen3", suffix: "-rs"},
        {text: "Diamond/Pearl/Platinum/SoulSilver/HeartGold", gen: "gen4", suffix: "-dp"}
      ],
      generationSelection: null,
      hms: [],
      tms: [],
      moveSelection: [],
      hmSelection: [],
      tmSelection: []
    }
  },

  methods: {
    clearPokemon: function(event) {
      this.pokemon.splice(0, this.pokemon.length);
    },

    movesChanged: function(event) {
      this.updatePokemonList();
    },

    generationChanged: function(event) {
      this.updateMoveList();
      this.updatePokemonList();
    },
    
    updateHmList: function(event) {
      this.hms.splice(0, this.hms.length);

      var genJson = json[this.generationSelection.gen];
      var hmsJson = genJson["hms"];
      var hmsInGen = Object.keys(hmsJson);

      hmsInGen.forEach((e) => {
        this.hms.push({name: e});
      });

      this.hmSelection = [];
    },
    
    updateTmList: function(event) {
      this.tms.splice(0, this.tms.length);
      
      var genJson = json[this.generationSelection.gen];
      var tmsJson = genJson["tms"];
      var tmsInGen = Object.keys(tmsJson);
      
      tmsInGen.forEach((e) => {
        this.tms.push({name: e});
      });

      this.tmSelection = [];
    },

    updateMoveList: function(event) {
      this.updateHmList(event);
      this.updateTmList(event);

      this.moveSelection = [];
    },

    updatePokemonList: function(event) {
      this.clearPokemon();
      
      this.moveSelection = this.hmSelection.concat(this.tmSelection);

      if (this.generationSelection === null || this.moveSelection == []) {
        return;
      }

      var movePokemon = [];
      var movesChecked = 0;
      
      this.moveSelection.forEach((move) => {
        if (movesChecked == 0) {
          var hmsPokemon = json[this.generationSelection.gen]["hms"][move];
          var tmsPokemon = json[this.generationSelection.gen]["tms"][move];
          movePokemon = [...hmsPokemon||[], ...tmsPokemon||[]].filter(Boolean);
        }
        else {
          var hmsPokemon = json[this.generationSelection.gen]["hms"][move];
          var tmsPokemon = json[this.generationSelection.gen]["tms"][move];
          var filterPokemon = [...hmsPokemon||[], ...tmsPokemon||[]].filter(Boolean);
          movePokemon = _.intersectionBy(movePokemon, filterPokemon, 'id');
        }
        movesChecked++;
      });
      
      movePokemon.forEach((e) => {
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
    overflow-y: scroll;
    height: 200%;
}

table {
    width: 100%;
}

th {
    width: 50%;
    color: white;
    padding-left: 40px;
    text-align: left;
    font-size: 1.5em;
}

td {
    vertical-align: top;
}

th {
    border-bottom: 2px solid white;
}

ul {
    margin-left: -40px;
}


</style>
