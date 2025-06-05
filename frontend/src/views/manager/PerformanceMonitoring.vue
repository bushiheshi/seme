<template>
    <div class="performance-monitoring-page">
        <h1>性能检测</h1>
        <div v-if="cpuPercent !== null">
            <p>CPU 使用率: {{ cpuPercent }}%</p>
            <p>内存使用率: {{ memoryPercent }}%</p>
            <p>内存总量: {{ memoryTotalGb }} GB</p>
            <p>已用内存: {{ memoryUsedGb }} GB</p>
        </div>
        <div v-else>
            <p>正在加载性能数据...</p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const cpuPercent = ref(null)
const memoryPercent = ref(null)
const memoryTotalGb = ref(null)
const memoryUsedGb = ref(null)

const fetchPerformanceData = async () => {
    try {
        const response = await axios.get('/api/performance/system')
        cpuPercent.value = response.data.cpu_percent
        memoryPercent.value = response.data.memory_percent
        memoryTotalGb.value = response.data.memory_total_gb
        memoryUsedGb.value = response.data.memory_used_gb
    } catch (error) {
        console.error('获取性能数据失败:', error)
    }
}

onMounted(() => {
    fetchPerformanceData()
})
</script>

<style scoped>
.performance-monitoring-page {
    padding: 20px;
}
</style> 