# Ansible Playbook 项目

一个完整的 Ansible Playbook 项目示例，展示了标准的目录结构和最佳实践。

## 📁 项目结构

```
my-ansible-project/
├── ansible.cfg                    # Ansible 配置文件
├── inventory                      # 主机清单文件
├── site.yml                       # 主 Playbook 文件
├── group_vars/                    # 组变量目录
│   ├── all.yml                   # 所有主机的通用变量
│   └── webservers.yml            # webservers 组的特定变量
├── host_vars/                     # 主机变量目录
│   └── web1.yml                  # web1 主机的特定变量
├── roles/                         # 角色目录
│   └── nginx/                    # nginx 角色
│       ├── tasks/                # 任务目录
│       │   └── main.yml          # 角色主任务文件
│       ├── handlers/             # 处理器目录
│       │   └── main.yml          # 角色处理器文件
│       ├── templates/             # 模板目录
│       │   └── nginx.conf.j2     # Nginx 配置文件模板
│       ├── files/                 # 文件目录
│       │   └── custom-index.html # 静态文件（自定义首页）
│       ├── vars/                  # 角色变量目录
│       │   └── main.yml          # 角色专用变量
│       ├── defaults/              # 默认变量目录
│       │   └── main.yml          # 角色默认变量（可被覆盖）
│       └── meta/                  # 元数据目录
│           └── main.yml          # 角色依赖和元信息
├── files/                         # 全局文件目录
│   └── global-config.txt         # 全局静态文件
├── templates/                     # 全局模板目录
│   └── motd.j2                   # 全局模板文件
└── library/                       # 自定义模块目录
    └── custom_module.py          # 自定义 Ansible 模块
```

## 🚀 快速开始

### 前提条件

- Ansible 2.9+
- Python 3.6+
- 访问目标主机的 SSH 权限

### 基本用法

```bash
# 克隆项目
git clone <repository-url>
cd my-ansible-project

# 语法检查
ansible-playbook --syntax-check site.yml

# 试运行（不实际执行）
ansible-playbook --check site.yml

# 实际运行
ansible-playbook site.yml

# 指定 inventory 文件
ansible-playbook -i inventory site.yml
```

## 📋 文件详解

### 配置文件

#### `ansible.cfg`
Ansible 主配置文件，设置默认参数和全局选项。

**引用位置**: 所有 Ansible 命令自动读取

#### `inventory`
定义管理的主机和主机组，包含连接信息和分组。

**引用位置**: 通过 `ansible.cfg` 或 `-i` 参数指定

#### `site.yml`
主 Playbook 文件，定义执行流程和任务组织。

**引用位置**: 直接运行 `ansible-playbook site.yml`

### 变量管理

#### `group_vars/all.yml`
所有主机共用的全局变量。

**变量示例**:
```yaml
timezone: UTC
admin_email: admin@company.com
package_list:
  - curl
  - wget
  - vim
```

#### `group_vars/webservers.yml`
webservers 主机组特有的变量。

**变量示例**:
```yaml
nginx_port: 80
server_name: "example.com"
max_workers: 4
```

#### `host_vars/web1.yml`
特定主机（web1）的专用变量。

**变量示例**:
```yaml
server_name: "web1.example.com"
custom_port: 8080
is_primary: true
```

### 角色系统 (roles/nginx/)

#### `tasks/main.yml`
定义 nginx 角色的执行任务序列。

**任务示例**:
- 安装 Nginx 软件包
- 配置模板文件
- 复制静态文件
- 启动并启用服务

#### `handlers/main.yml`
定义任务触发的处理器，如服务重启。

**处理器示例**:
```yaml
- name: restart nginx
  service:
    name: nginx
    state: restarted
```

#### `templates/nginx.conf.j2`
Nginx 配置模板文件，使用 Jinja2 语法支持动态内容。

**模板特性**:
- 变量替换：`{{ nginx_port }}`
- 条件判断
- 循环迭代

#### `files/custom-index.html`
静态文件资源，直接复制到目标主机。

**使用方式**: 通过 `copy` 模块引用

#### `vars/main.yml`
角色专用变量，具有较高优先级。

#### `defaults/main.yml`
角色默认变量，可被其他变量文件覆盖。

#### `meta/main.yml`
角色元信息和依赖关系定义。

### 全局资源

#### `files/global-config.txt`
全局静态文件，任何任务都可引用。

**引用方式**: `src: "files/global-config.txt"`

#### `templates/motd.j2`
全局模板文件，支持所有主机的动态内容生成。

**引用方式**: `src: "templates/motd.j2"`

## 🔧 自定义模块

### `library/custom_module.py`

扩展 Ansible 功能的自定义模块示例。

#### 模块结构

```python
#!/usr/bin/python3
from ansible.module_utils.basic import AnsibleModule

def main():
    # 定义模块参数
    module = AnsibleModule(
        argument_spec=dict(
            message=dict(type='str', required=True),
            repeat=dict(type='int', default=1)
        )
    )
    
    # 业务逻辑处理
    message = module.params['message']
    repeat = module.params['repeat']
    
    result = dict(
        changed=False,
        original_message=message,
        repeated_message=message * repeat,
        message="Task completed successfully"
    )
    
    module.exit_json(**result)

if __name__ == '__main__':
    main()
```

#### 在 Playbook 中使用

```yaml
- name: 使用自定义模块示例
  hosts: all
  tasks:
    - name: 调用自定义模块
      custom_module:
        message: "Hello World"
        repeat: 3
      register: custom_result

    - name: 显示自定义模块结果
      debug:
        var: custom_result
```

#### 输出结果

```json
{
  "changed": false,
  "original_message": "Hello World",
  "repeated_message": "Hello WorldHello WorldHello World",
  "message": "Task completed successfully"
}
```

## 🎯 执行流程

### 任务执行顺序

1. **配置加载**: 读取 `ansible.cfg` 设置
2. **清单解析**: 加载 `inventory` 文件
3. **变量加载**: 按优先级加载所有变量文件
4. **Play 执行**: 按 `site.yml` 定义的顺序执行
5. **角色调用**: 执行角色中的任务和处理器
6. **资源应用**: 使用模板和文件目录中的资源

### 变量优先级（从高到低）

1. `host_vars/` - 主机特定变量
2. `group_vars/` - 组变量
3. `roles/*/vars/` - 角色变量
4. `roles/*/defaults/` - 角色默认变量
5. `group_vars/all.yml` - 全局变量

## 📝 最佳实践

### 目录结构建议

- 使用角色组织相关任务
- 按环境分离 inventory 文件
- 合理使用变量优先级
- 保持模板和文件的分离

### 代码组织技巧

- 一个角色负责一个服务或应用
- 使用 handlers 处理服务重启
- 模板文件使用 `.j2` 扩展名
- 为复杂操作创建自定义模块

## 🔍 故障排除

### 常见问题

**语法错误检查**:
```bash
ansible-playbook --syntax-check site.yml
```

**变量调试**:
```bash
ansible -i inventory all -m debug -a "var=hostvars[inventory_hostname]"
```

**连接测试**:
```bash
ansible -i inventory all -m ping
```

### 调试技巧

1. 使用 `-v`、`-vv`、`-vvv` 参数增加输出详细程度
2. 添加 `--check` 模式进行试运行
3. 使用 `--tags` 和 `--skip-tags` 选择性执行任务

## 🤝 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢 Ansible 社区提供的优秀文档和示例
- 感谢所有贡献者和用户的支持

---

**Happy Automating!** 🚀