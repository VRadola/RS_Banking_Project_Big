<script setup>
import {computed} from "vue";
import {useToasts} from "../stores/toasts";

const store = useToasts();
const items = computed(() => store.items);
</script>

<template>
  <div style="position:fixed; right:16px; top:16px; z-index:9999; display:flex; flex-direction:column; gap:10px;">
    <div
      v-for="t in items"
      :key="t.id"
      class="card"
      style="min-width:280px; padding:12px 12px; border-radius:16px;"
    >
      <div style="display:flex; justify-content:space-between; gap:12px; align-items:flex-start;">
        <div>
          <div style="font-weight:700; margin-bottom:4px;">
            <span v-if="t.type==='success'" style="color:var(--good);">●</span>
            <span v-else-if="t.type==='error'" style="color:var(--bad);">●</span>
            <span v-else style="color:var(--warn);">●</span>
            {{ t.title }}
          </div>
          <div class="muted" style="font-size:13px;">{{ t.message }}</div>
        </div>
        <button class="btn" style="padding:6px 10px;" @click="store.remove(t.id)">✕</button>
      </div>
    </div>
  </div>
</template>