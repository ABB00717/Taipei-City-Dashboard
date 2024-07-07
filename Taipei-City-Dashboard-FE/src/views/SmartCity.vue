<template>
	<div class="chat-container">
		<h1>智慧城<a class="easter-egg"
				href="https://narutonti.com/wp-content/uploads/2013/08/naruto47-015_mini-e1376513163291.jpg">市聊天室</a>
		</h1>
		<div class="messages" ref="messagesContainer">
			<div v-for="(message, index) in chatStore.state.chatHistory" :key="index"
				:class="['message', message.role]">
				{{ message.content }}
			</div>
			<img class="spinningCat" v-if="isLoading" src="./loading_cat.gif">
		</div>
		<div class="input-area">
			<textarea v-model="prompt" :disabled="isLoading" placeholder="在這裡輸入你的問題..."
				@keydown.enter.shift.exact="handleShiftEnter" @keydown.enter.exact="generateResponse"></textarea>
			<button @click="handleButtonClick" :disabled="isLoading">
				<i v-if="isLoading" class="fa-solid fa-spinner"></i>
				<i v-else class="fa-regular fa-paper-plane"></i>
			</button>
		</div>
	</div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { useChatStore } from './useChatStore'

export default {
	name: 'SmartCity',
	setup() {
		const prompt = ref('')
		const isLoading = ref(false)
		const messagesContainer = ref(null)
		const chatStore = useChatStore()
		const clicks = ref(0)
		const timer = ref(null)

		const scrollToBottom = () => {
			nextTick(() => {
				if (messagesContainer.value) {
					messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
				}
			})
		}

		const generateResponse = async () => {
			if (!prompt.value.trim()) return
			isLoading.value = true

			chatStore.addMessage({ role: 'user', content: prompt.value })
			scrollToBottom()
			try {
				const response = await fetch('http://localhost:5001/generate', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({
						prompt: prompt.value,
						session_id: 'user123'  // 使用唯一的會話 ID
					})
				})

				const data = await response.json()
				isLoading.value = false

				if (!response.ok) {
					throw new Error(`API 錯誤: ${data.error || response.statusText}`)
				}

				chatStore.addMessage({ role: 'assistant', content: data.response })
				scrollToBottom()
			} catch (error) {
				console.error('Error:', error)
				chatStore.addMessage({ role: 'assistant', content: '抱歉，發生錯誤。請稍後再試。' })
				scrollToBottom()
			} finally {
				isLoading.value = false
				prompt.value = ''
			}
		}

		const handleButtonClick = () => {
			clicks.value += 1

			if (timer.value) {
				clearTimeout(timer.value)
			}

			timer.value = setTimeout(() => {
				if (clicks.value > 1) {
					console.log("TOO MUCH")
					chatStore.addMessage({ role: 'assistant', content: "Redirecting you to https://cpstest.org/" })
					window.location.href = 'https://cpstest.org/'
				} else {
					generateResponse()
				}
				clicks.value = 0
				timer.value = null
			}, 100)
		}

		const handleShiftEnter = (event) => {
			return
		}

		onMounted(() => {
			scrollToBottom()
		})

		return {
			prompt,
			clicks,
			timer,
			isLoading,
			generateResponse,
			messagesContainer,
			chatStore,
			handleShiftEnter,
			handleButtonClick
		}
	}
}
</script>

<style scoped>
.chat-container {
	font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
	max-width: 800px;
	align-content: center;
	margin: 20px auto;
	background: var(--chat-bg-light);
	border-radius: 8px;
	box-shadow: 0 0 10px 10px rgba(0, 0, 0, 0.1);
	padding: 20px;
	box-shadow: #333;
}

h1 {
	color: var(--chat-text-light);
	text-align: center;
	margin-bottom: 20px;
}

.messages {
	height: 50vh;
	padding: 10px;
	border: 2px solid #e1e4e8;
	border-radius: 8px;
	margin-bottom: 20px;
	overflow: hidden;
	overflow-y: scroll;
}

.message {
	display: flex;
	width: fit-content;
	max-width: 100%;
	margin-bottom: 10px;
	padding: 8px 12px;
	border-radius: 18px;
	word-wrap: break-word;
}

.user {
	justify-content: flex-end;
	background-color: #007bff;
	color: white;
	margin-left: auto;
	margin-right: 1em;
	max-width: 60%;
	word-wrap: break-word;
	animation-name: popup;
	animation-duration: 0.3s;
	animation-timing-function: ease-in-out;
}

.user:active {
	animation-name: shake;
	animation-duration: 0.3s;
	animation-timing-function: ease-in-out;

}

.assistant {
	justify-content: flex-start;
	background-color: white;
	color: #333;
	margin-right: auto;
	margin-left: 1em;
	max-width: 60%;
	word-wrap: break-word;
	animation-name: popup;
	animation-duration: 0.3s;
	animation-timing-function: ease-in-out;
}

.assistant:active {
	animation-name: shake;
	animation-duration: 0.3s;
	animation-timing-function: ease-in-out;

}

@keyframes popup {
	0% {
		transform: scale(0.4);
	}

	33% {
		transform: scale(1.1);
	}

	100% {
		transform: scale(1);
	}
}

@keyframes shake {
	0% {
		transform: translate(5px, 3px);
	}

	25% {
		transform: translate(-2px, 1px);
	}

	50% {
		transform: translate(4px, -3px);
	}

	75% {
		transform: translate(1px, 2px);
	}

	100% {
		transform: translate(0px, 0px);
	}
}

.input-area {
	display: flex;
	flex-direction: column;
	overflow: visible;
}

textarea {
	field-sizing: content;
	width: 100%;
	min-height: 5vh;
	max-height: 15vh;
	border-radius: 4px;
	margin-bottom: 10px;
	resize: none;
	animation-name: slidein;
	animation-duration: 1s;
	animation-delay: 0.3s;
	outline: 1px solid #e1e4e8;
	border-radius: 8px;
	transition: border 0.3s;
}

textarea:focus {
	outline: none;
	border: 1px solid #007bff;
	box-shadow: 0px 0px 5px #007bff;
	-moz-box-shadow: 0px 0px 5px #007bff;
	-webkit-box-shadow: 0px 0px 5px #007bff;
}

button {
	background-color: #28a745;
	color: white;
	border: none;
	padding: 10px 20px;
	border-radius: 4px;
	cursor: pointer;
	align-self: flex-end;
	transition: background-color 0.3s;
}

button:hover {
	background-color: #218838;
	animation: glowing 3000ms infinite;
}

button:active {
	background-color: #145222;
	transform: scale(0.95, 0.95);
	transition-duration: 0.3s;
}

button:disabled {
	background-color: #6c757d;
	cursor: not-allowed;
	animation: none !important;
}

.spinningCat {
	margin-left: 22px;
	width: 100px;
	height: 100px;
}

@keyframes glowing {
	0% {
		background-color: #2ba805;
		box-shadow: 0 0 5px #2ba805;
	}

	50% {
		background-color: #49e819;
		box-shadow: 0 0 20px #49e819;
	}

	100% {
		background-color: #2ba805;
		box-shadow: 0 0 5px #2ba805;
	}
}

a.easter-egg:hover {
	text-decoration: underline;
}
</style>