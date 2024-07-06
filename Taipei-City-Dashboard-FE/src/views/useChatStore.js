import { reactive } from 'vue'

const state = reactive({
  chatHistory: []
})

export function useChatStore() {
  const addMessage = (message) => {
    state.chatHistory.push(message)
  }

  return {
    state,
    addMessage
  }
}
