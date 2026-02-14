import {reactive} from "vue";

const state = reactive({
  items: [],
});

export function useToasts() {
  function push({ type = "success", title = "OK", message = "" }) {
    const id = crypto.randomUUID();
    state.items.unshift({ id, type, title, message });
    setTimeout(() => remove(id), 3500);
  }

  function remove(id) {
    const idx = state.items.findIndex((x) => x.id === id);
    if (idx >= 0) state.items.splice(idx, 1);
  }

  return {
    items: state.items,
    push,
    remove,
  };
}