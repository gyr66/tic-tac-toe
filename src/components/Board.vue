<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="board">
    <div
      class="cell"
      v-for="(cell, index) in board.flat()"
      :key="index"
      @click="handleCellClicked(index)"
    >
      <img :src="O" class="mark" v-if="cell === 1" />
      <img :src="X" class="mark" v-else-if="cell === -1" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, toRaw, watch } from 'vue'
import O from '../assets/O.png'
import X from '../assets/X.png'
import { alphaBetaSearch, isTerminal, utility } from '../game'

const board = reactive([
  [0, 0, 0],
  [0, 0, 0],
  [0, 0, 0]
])
const status = ref<'playing' | 'win' | 'lose' | 'draw'>('playing')

const emit = defineEmits(['stateChange'])

const handleCellClicked = (index: number) => {
  const row = Math.floor(index / 3)
  const col = index % 3
  if (board[row][col]) return
  const { ones, minusOnes } = board.flat().reduce(
    (acc, num) => {
      if (num === 1) acc.ones++
      if (num === -1) acc.minusOnes++
      return acc
    },
    { ones: 0, minusOnes: 0 }
  )
  if (status.value === 'playing' && ones === minusOnes) {
    board[row][col] = -1
    const pos = alphaBetaSearch(toRaw(board))
    if (pos[0] >= 0 && pos[0] < 3 && pos[1] >= 0 && pos[1] < 3) {
      board[pos[0]][pos[1]] = 1
    }
  }
}

watch(
  board,
  () => {
    if (isTerminal(toRaw(board))) {
      const v = utility(toRaw(board))
      if (v === 1) status.value = 'lose'
      else if (v === -1) status.value = 'win'
      else status.value = 'draw'
    } else status.value = 'playing'
    emit('stateChange', board.values, status.value)
  },
  { immediate: true }
)

const reset = () => {
  for (let i = 0; i < 3; i++) {
    board[i].fill(0)
  }
}

defineExpose({ board, status, reset })
</script>

<style scoped>
.board {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  border-left: 1px solid #000;
  border-top: 1px solid #000;
}

.cell {
  aspect-ratio: 1 / 1;
  border-right: 1px solid #000;
  border-bottom: 1px solid #000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.mark {
  width: 60%;
  height: 60%;
}
</style>
