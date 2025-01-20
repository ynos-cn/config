#!/bin/bash

# 定义服务名称和 Docker Compose 文件路径
FRONTEND_COMPOSE="docker-compose.web.yml"
BACKEND_COMPOSE="docker-compose.service.yml"
FRONTEND_NAME="config_web"
BACKEND_NAME="config_service"

# 定义颜色输出
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
RESET="\033[0m"

# 输出信息的函数
function echo_info() { echo -e "${GREEN}[INFO] $1${RESET}"; }
function echo_warning() { echo -e "${YELLOW}[WARNING] $1${RESET}"; }
function echo_error() { echo -e "${RED}[ERROR] $1${RESET}"; }

# 更新子模块内容
function update_submodules() {
    echo_info "更新子模块内容..."
    git submodule update --init --recursive
}

# 构建前端镜像
function build_frontend() {
    echo_info "开始构建前端镜像..."
    update_submodules
    docker-compose -f $FRONTEND_COMPOSE build $FRONTEND_NAME
}

# 构建后端镜像
function build_backend() {
    echo_info "开始构建后端镜像..."
    update_submodules
    docker-compose -f $BACKEND_COMPOSE build $BACKEND_NAME
}

# 启动前端服务
function start_frontend() {
    echo_info "启动前端服务..."
    docker-compose -f $FRONTEND_COMPOSE up -d
}

# 启动后端服务
function start_backend() {
    echo_info "启动后端服务..."
    docker-compose -f $BACKEND_COMPOSE up -d
}

# 停止前端服务
function stop_frontend() {
    echo_info "停止前端服务..."
    docker-compose -f $FRONTEND_COMPOSE down
}

# 停止后端服务
function stop_backend() {
    echo_info "停止后端服务..."
    docker-compose -f $BACKEND_COMPOSE down
}

# 查看当前运行的容器
function list_containers() {
    echo_info "查看当前运行的容器..."
    docker ps
}

# 更新前端服务
function update_frontend() {
    echo_info "更新前端服务..."
    stop_frontend
    build_frontend
    start_frontend
}

# 更新后端服务
function update_backend() {
    echo_info "更新后端服务..."
    stop_backend
    build_backend
    start_backend
}

# 重启前端服务
function restart_frontend() {
    echo_info "重启前端服务..."
    docker-compose -f $FRONTEND_COMPOSE restart
}

# 重启后端服务
function restart_backend() {
    echo_info "重启后端服务..."
    docker-compose -f $BACKEND_COMPOSE restart
}

# 健康检查
function health_check() {
    echo_info "检查容器健康状态..."
    docker-compose -f $BACKEND_COMPOSE ps
    docker-compose -f $FRONTEND_COMPOSE ps
}

# 同时构建并部署前后端服务
function build_deploy() {
    echo_info "开始同时构建并部署前后端服务..."

    # 停止前后端服务
    stop_frontend
    stop_backend

    # 构建前端和后端镜像
    build_backend
    build_frontend

    # 启动前后端服务
    start_backend
    start_frontend
}

# 零停机更新前端服务
function zero_downtime_update_frontend() {
    echo_info "执行零停机更新前端服务..."

    # 构建新的前端镜像
    build_frontend

    # 启动一个新的容器实例并保持旧容器运行
    docker-compose -f $FRONTEND_COMPOSE up -d --no-deps --scale $FRONTEND_NAME=2

    # 等待新容器启动（这里假设需要20秒，但请根据实际情况调整）
    sleep 20

    # 健康检查确保新容器正常
    if ! docker-compose -f $FRONTEND_COMPOSE exec $FRONTEND_NAME curl -f http://localhost:80; then
        echo_error "新前端容器健康检查失败"
        docker-compose -f $FRONTEND_COMPOSE stop $FRONTEND_NAME
        docker-compose -f $FRONTEND_COMPOSE up -d --no-deps --scale $FRONTEND_NAME=1
        exit 1
    fi

    # 停止旧容器
    docker-compose -f $FRONTEND_COMPOSE stop $FRONTEND_NAME
    docker-compose -f $FRONTEND_COMPOSE rm -f $FRONTEND_NAME

    # 确保只运行一个新容器
    docker-compose -f $FRONTEND_COMPOSE up -d --no-deps --scale $FRONTEND_NAME=1
}

# 零停机更新后端服务
function zero_downtime_update_backend() {
    echo_info "执行零停机更新后端服务..."

    # 构建新的后端镜像
    build_backend

    # 启动一个新的容器实例并保持旧容器运行
    docker-compose -f $BACKEND_COMPOSE up -d --no-deps --scale $BACKEND_NAME=2

    # 等待新容器启动（这里假设需要20秒，但请根据实际情况调整）
    sleep 20

    # 健康检查确保新容器正常
    if ! docker-compose -f $BACKEND_COMPOSE exec $BACKEND_NAME curl -f http://localhost:8891/config/api/isStart; then
        echo_error "新后端容器健康检查失败"
        docker-compose -f $BACKEND_COMPOSE stop $BACKEND_NAME
        docker-compose -f $BACKEND_COMPOSE up -d --no-deps --scale $BACKEND_NAME=1
        exit 1
    fi

    # 停止旧容器
    docker-compose -f $BACKEND_COMPOSE stop $BACKEND_NAME
    docker-compose -f $BACKEND_COMPOSE rm -f $BACKEND_NAME

    # 确保只运行一个新容器
    docker-compose -f $BACKEND_COMPOSE up -d --no-deps --scale $BACKEND_NAME=1
}

# 同时零停机更新前后端服务
function zero_downtime_update() {
    echo_info "执行零停机更新前后端服务..."

    zero_downtime_update_backend
    zero_downtime_update_frontend
}

# 显示脚本使用说明
function usage() {
    echo -e "Usage: $0 {start | stop | restart | build | update | status | health | zero_downtime_update | zero_downtime_update_frontend | zero_downtime_update_backend | build_deploy} [web|services]"
    echo -e "  start web | services - 启动前端或后端服务"
    echo -e "  stop web | services  - 停止前端或后端服务"
    echo -e "  restart web | services - 重启前端或后端服务"
    echo -e "  build web | services - 构建前端或后端镜像"
    echo -e "  update web | services - 更新前端或后端服务"
    echo -e "  zero_downtime_update - 同时执行零停机更新前后端服务"
    echo -e "  zero_downtime_update_frontend - 同时执行零停机更新前端服务"
    echo -e "  zero_downtime_update_backend - 同时执行零停机更新后端服务"
    echo -e "  build_deploy - 同时构建并部署前后端服务"
    echo -e "  status - 查看当前运行的容器"
    echo -e "  health - 健康检查容器"
}

# 判断传入参数并执行相应操作
if [ -z "$1" ]; then
    usage
    exit 1
fi

case "$1" in
start)
    if [ -z "$2" ]; then
        echo_error "请指定要启动的服务：web 或 services"
        exit 1
    fi
    case "$2" in
    web)
        start_frontend
        ;;
    services)
        start_backend
        ;;
    *)
        echo_error "无效的服务：$2"
        usage
        exit 1
        ;;
    esac
    ;;
stop)
    if [ -z "$2" ]; then
        echo_error "请指定要停止的服务：web 或 services"
        exit 1
    fi
    case "$2" in
    web)
        stop_frontend
        ;;
    services)
        stop_backend
        ;;
    *)
        echo_error "无效的服务：$2"
        usage
        exit 1
        ;;
    esac
    ;;
restart)
    if [ -z "$2" ]; then
        echo_error "请指定要重启的服务：web 或 services"
        exit 1
    fi
    case "$2" in
    web)
        restart_frontend
        ;;
    services)
        restart_backend
        ;;
    *)
        echo_error "无效的服务：$2"
        usage
        exit 1
        ;;
    esac
    ;;
build)
    if [ -z "$2" ]; then
        echo_error "请指定要构建的服务：web 或 services"
        exit 1
    fi
    case "$2" in
    web)
        build_frontend
        ;;
    services)
        build_backend
        ;;
    *)
        echo_error "无效的服务：$2"
        usage
        exit 1
        ;;
    esac
    ;;
update)
    if [ -z "$2" ]; then
        echo_error "请指定要更新的服务：web 或 services"
        exit 1
    fi
    case "$2" in
    web)
        update_frontend
        ;;
    services)
        update_backend
        ;;
    *)
        echo_error "无效的服务：$2"
        usage
        exit 1
        ;;
    esac
    ;;
zero_downtime_update)
    zero_downtime_update
    ;;

zero_downtime_update_backend)
    zero_downtime_update_backend
    ;;

zero_downtime_update_frontend)
    zero_downtime_update_frontend
    ;;

build_deploy)
    build_deploy
    ;;
status)
    list_containers
    ;;
health)
    health_check
    ;;
*)
    usage
    exit 1
    ;;
esac
