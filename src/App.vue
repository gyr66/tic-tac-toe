<script setup lang="ts">
import { ref } from 'vue'
import Board from './components/Board.vue'

const board = ref<InstanceType<typeof Board> | null>(null)

const status = ref<'playing' | 'win' | 'lose' | 'draw'>()

const handleStateChanged = (_: number[][], s: 'playing' | 'win' | 'lose' | 'draw') => {
  status.value = s
}

const handleResetButtonClicked = () => {
  board.value?.reset()
}
</script>

<template>
  <div class="wrapper">
    <header class="header">
      <h1>tic-tac-toe</h1>
      <p v-if="status === 'playing'">Your turn</p>
      <p v-else-if="status === 'win'">You win!</p>
      <p v-else-if="status === 'lose'">You lose!</p>
      <p v-else-if="status === 'draw'">Draw!</p>
    </header>
    <main class="main">
      <board class="board" ref="board" @stateChange="handleStateChanged" />
      <button class="reset" @click="handleResetButtonClicked">Reset</button>
    </main>
  </div>
</template>

<style scoped>
.header {
  text-align: center;
  font-size: 24px;
}

.main {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  text-align: center;
}
.board {
  width: 100%;
  height: 100%;
}

.reset {
  width: 10rem;
  height: 2rem;
  margin-top: 2rem;
}
</style>
