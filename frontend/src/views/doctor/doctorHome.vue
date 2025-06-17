<template>
    <el-container class="layout-container">
        <!-- 左侧导航栏 -->
        <el-aside width="220px" class="side-nav">
            <div class="side-header">
                <span class="system-title">前列腺消融手术预后疗效预测系统</span>
            </div>
            <el-menu
                :default-active="activeMenu"
                class="nav-menu"
                router
                :collapse="false"
                background-color="#fff9e6"
                text-color="#304156"
                active-text-color="#409EFF"
            >
                <el-menu-item index="/patient-management">
                    <el-icon><User /></el-icon>
                    <span>患者管理</span>
                </el-menu-item>
                <el-menu-item index="/effect-prediction">
                    <el-icon><DataLine /></el-icon>
                    <span>效果预测</span>
                </el-menu-item>
                <el-menu-item index="/prediction-records">
                    <el-icon><Document /></el-icon>
                    <span>预测记录</span>
                </el-menu-item>
            </el-menu>
            <div class="side-footer">
                <el-dropdown @command="handleCommand">
                    <span class="el-dropdown-link">
                        <el-avatar :size="32" :src="doctorInfo.avatar || defaultAvatar" />
                        <span class="doctor-name">{{ doctorInfo.name }}</span>
                        <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </el-aside>
        <!-- 右侧内容区 -->
        <el-main class="main-content">
            <!-- 欢迎信息卡片，只在首次登录时显示 -->
            <el-card v-if="showWelcome" class="welcome-card">
                <template #header>
                    <div class="welcome-header">
                        <span>欢迎回来，{{ doctorInfo.name }} 医生</span>
                        <el-button
                            type="text"
                            class="close-button"
                            @click="closeWelcome"
                        >
                            <el-icon><Close /></el-icon>
                        </el-button>
                    </div>
                </template>
                <div class="welcome-content">
                    <p>您可以通过左侧导航栏访问以下功能：</p>
                    <ul>
                        <li><b>患者管理：</b>管理患者信息和病历</li>
                        <li><b>效果预测：</b>进行手术预后效果预测</li>
                        <li><b>预测记录：</b>查看历史预测记录</li>
                    </ul>
                </div>
            </el-card>

            <!-- 预测步骤引导卡片 -->
            <el-card class="guide-card">
                <template #header>
                    <div class="guide-header">
                        <el-icon class="guide-icon"><Guide /></el-icon>
                        <span>预测操作指南</span>
                    </div>
                </template>
                <el-steps :active="1" finish-status="success" direction="vertical" class="prediction-steps">
                    <el-step title="第一步：选择患者" description="在患者管理页面选择需要进行预测的患者，或添加新患者信息。">
                        <template #icon>
                            <el-icon><User /></el-icon>
                        </template>
                    </el-step>
                    <el-step title="第二步：上传MRI序列" description="在患者详情页面，点击'MRI序列管理'按钮，上传患者的MRI序列图像。">
                        <template #icon>
                            <el-icon><Upload /></el-icon>
                        </template>
                    </el-step>
                    <el-step title="第三步：进行预测" description="在效果预测页面，选择已上传的MRI序列，系统将自动进行预后效果预测。">
                        <template #icon>
                            <el-icon><DataLine /></el-icon>
                        </template>
                    </el-step>
                    <el-step title="第四步：查看结果" description="预测完成后，可以查看详细的预测结果，并可在预测记录中查看历史预测记录。">
                        <template #icon>
                            <el-icon><Document /></el-icon>
                        </template>
                    </el-step>
                </el-steps>
            </el-card>

            <!-- 路由视图，用于显示各个功能页面 -->
            <router-view v-slot="{ Component }">
                <transition name="fade" mode="out-in">
                    <component :is="Component" />
                </transition>
            </router-view>
        </el-main>
    </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, DataLine, Document, ArrowDown, Close, Guide, Upload } from '@element-plus/icons-vue'

const router = useRouter()
const activeMenu = ref('/patient-management')
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
const showWelcome = ref(true)

// 获取医生信息
const doctorInfo = ref({})
onMounted(() => {
    const storedInfo = localStorage.getItem('doctorInfo')
    if (storedInfo) {
        doctorInfo.value = JSON.parse(storedInfo)
    }
    // 默认跳转到患者管理页面
    router.push('/patient-management')
})

// 关闭欢迎卡片
const closeWelcome = () => {
    showWelcome.value = false
}

// 处理下拉菜单命令
const handleCommand = (command) => {
    switch (command) {
        case 'profile':
            router.push('/doctor-profile')
            break
        case 'logout':
            ElMessageBox.confirm(
                '确定要退出登录吗？',
                '提示',
                {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }
            ).then(() => {
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('doctorInfo')
                router.replace('/login')
                ElMessage.success('已退出登录')
            }).catch(() => {})
            break
    }
}
</script>

<style scoped>
.layout-container {
    height: 100vh;
    display: flex;
    flex-direction: row;
    background: linear-gradient(120deg, #fffbe6 60%, #fff9e6 100%);
}

.side-nav {
    background: #fff9e6;
    box-shadow: 4px 0 24px 0 rgba(247, 200, 115, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 0;
    border-top-right-radius: 32px;
    border-bottom-right-radius: 32px;
    min-width: 220px;
    max-width: 260px;
    transition: box-shadow 0.3s;
}

.side-header {
    padding: 40px 0 24px 0;
    text-align: center;
}

.system-title {
    font-size: 20px;
    font-weight: bold;
    color: #e6a23c;
    letter-spacing: 2px;
    text-shadow: 0 2px 8px #fff3d1;
}

.nav-menu {
    border-right: none;
    background: transparent;
    margin-top: 32px;
}

.nav-menu .el-menu-item {
    height: 54px;
    line-height: 54px;
    font-size: 17px;
    color: #304156;
    border-radius: 12px;
    margin: 0 16px 16px 16px;
    transition: background 0.2s, color 0.2s, box-shadow 0.2s;
    font-weight: 500;
    letter-spacing: 1px;
    box-shadow: 0 2px 8px rgba(255, 231, 165, 0.08);
}

.nav-menu .el-menu-item.is-active {
    background: linear-gradient(90deg, #ffe7a5 60%, #fffbe6 100%);
    color: #e6a23c !important;
    box-shadow: 0 4px 16px #ffe7a5;
}

.nav-menu .el-menu-item:hover {
    background: #fffbe6;
    color: #e6a23c;
}

.side-footer {
    padding: 32px 0 40px 0;
    text-align: center;
}

.el-dropdown-link {
    display: flex;
    align-items: center;
    cursor: pointer;
    color: #606266;
    justify-content: center;
    background: #fffbe6;
    border-radius: 16px;
    padding: 10px 18px;
    box-shadow: 0 2px 8px #ffe7a5;
    transition: box-shadow 0.2s;
}

.el-dropdown-link:hover {
    color: #e6a23c;
    box-shadow: 0 4px 16px #ffe7a5;
}

.el-avatar {
    margin-right: 10px;
    border: 2px solid #ffe7a5;
    box-shadow: 0 2px 8px #ffe7a5;
}

.doctor-name {
    font-size: 16px;
    font-weight: 600;
    color: #304156;
    margin-right: 6px;
    letter-spacing: 1px;
}

.main-content {
    background: linear-gradient(120deg, #fffbe6 80%, #fff9e6 100%);
    padding: 40px 40px 40px 40px;
    flex: 1;
    overflow-y: auto;
    min-width: 0;
    border-radius: 32px;
    box-shadow: 0 4px 32px 0 rgba(247, 200, 115, 0.06);
}

.welcome-card, .guide-card {
    border-radius: 18px;
    box-shadow: 0 4px 24px 0 rgba(247, 200, 115, 0.10);
    margin-bottom: 28px;
    background: #fffef6;
    border: 1.5px solid #ffe7a5;
}

.welcome-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 18px;
    color: #e6a23c;
    font-weight: 600;
}

.welcome-content {
    color: #606266;
    font-size: 16px;
    padding: 8px 0 0 0;
}

.welcome-content ul {
    margin-top: 10px;
    padding-left: 24px;
}

.welcome-content li {
    margin-bottom: 10px;
    font-size: 15px;
}

.close-button {
    padding: 2px;
    color: #e6a23c;
}

.guide-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 18px;
    color: #e6a23c;
    font-weight: 600;
}

.guide-icon {
    font-size: 22px;
    color: #e6a23c;
}

.prediction-steps {
    padding: 24px 16px 8px 16px;
}

.prediction-steps :deep(.el-step__title) {
    font-size: 16px;
    font-weight: bold;
    color: #e6a23c;
}

.prediction-steps :deep(.el-step__description) {
    font-size: 15px;
    color: #606266;
    margin-top: 8px;
}

.prediction-steps :deep(.el-step__icon) {
    background: linear-gradient(135deg, #ffe7a5 60%, #fffbe6 100%);
    color: #e6a23c;
    border-radius: 50%;
    font-size: 22px;
    box-shadow: 0 2px 8px #ffe7a5;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
