# 更新后的 README.md

```markdown
# Ansible Playbook 项目

这是一个完整的 Ansible Playbook 项目示例，展示了标准的目录结构和最佳实践。

## 项目结构

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

## 文件作用详解

### 根目录文件

**ansible.cfg**
- Ansible 配置文件，设置默认参数
- 运行任何 Ansible 命令时自动读取
- 配置内容：Inventory 路径、远程用户、SSH 设置、权限提升等

**inventory**
- 定义管理的主机和主机组
- 在 ansible.cfg 中指定，或通过 `-i` 参数指定
- 包含：主机列表、分组、连接变量

**site.yml**
- 主 Playbook 文件，定义执行流程
- 直接运行 `ansible-playbook site.yml`
- 包含：Plays 列表，引用角色和任务

### 变量目录

**group_vars/all.yml**
- 定义所有主机共用的变量
- 自动加载到所有主机
- 示例变量：时区、管理员邮箱、通用软件包列表

**group_vars/webservers.yml**
- 定义 webservers 组特有的变量
- 自动加载到 webservers 组的所有主机
- 示例变量：Nginx 端口、服务器名称、工作进程数

**host_vars/web1.yml**
- 定义 web1 主机特有的变量
- 自动加载到 web1 主机
- 示例变量：特定端口、是否为主服务器、特殊配置

### 角色目录 (roles/nginx/)

**roles/nginx/tasks/main.yml**
- 定义 nginx 角色的执行任务
- 在 site.yml 中通过 `roles: [nginx]` 引用
- 包含任务：安装 Nginx、配置模板、复制文件、启动服务

**roles/nginx/handlers/main.yml**
- 定义任务触发的处理器（如服务重启）
- 在 tasks 中通过 `notify` 触发
- 示例：Nginx 配置变更后重启服务

**roles/nginx/templates/nginx.conf.j2**
- Nginx 配置模板文件，使用 Jinja2 语法
- 在 tasks 中通过 `template` 模块使用
- 特点：支持变量替换，生成动态配置文件

**roles/nginx/files/custom-index.html**
- 静态文件，直接复制到目标主机
- 在 tasks 中通过 `copy` 模块使用
- 特点：文件内容不变，直接传输

**roles/nginx/vars/main.yml**
- 定义 nginx 角色专用的变量
- 角色内部自动加载
- 特点：高优先级，用于角色特定配置

**roles/nginx/defaults/main.yml**
- 定义 nginx 角色的默认变量
- 角色内部自动加载
- 特点：低优先级，可被其他变量文件覆盖

**roles/nginx/meta/main.yml**
- 定义角色元信息和依赖关系
- Ansible Galaxy 和角色加载时使用
- 包含：作者信息、兼容平台、依赖角色

### 全局目录

**files/global-config.txt**
- 全局静态文件，任何任务都可引用
- 在 tasks 中通过 `copy` 模块使用 `src="files/..."`

**templates/motd.j2**
- 全局模板文件，任何任务都可引用
- 在 tasks 中通过 `template` 模块使用 `src="templates/..."`

**library/custom_module.py**
- 自定义 Ansible 模块
- 在 tasks 中通过模块名直接调用
- 特点：扩展 Ansible 功能，实现特定需求

## 关于 MySQL 任务

在最初的示例中，`site.yml` 包含了一个简单的 MySQL 安装任务：

```yaml
- name: 配置数据库服务器
  hosts: dbservers
  tasks:
    - name: 安装 MySQL
      apt:
        name: mysql-server
        state: present
      become: yes
```

**这个任务可以安全地移除**，因为：
1. 它只是一个演示不同主机组任务分配的示例
2. 在实际项目中，MySQL 应该作为一个完整的角色来实现
3. 移除它不会影响项目的核心功能演示

要移除 MySQL 任务，只需从 `site.yml` 中删除对应的 play 部分即可。

## 关于 Role 之后的任务执行

在 `site.yml` 中，nginx role 执行后还有一个任务：

```yaml
- name: 配置 Web 服务器
  hosts: webservers
  roles:
    - nginx
  tasks:
    - name: 复制全局配置文件
      copy:
        src: files/global-config.txt
        dest: /etc/global-config.txt
      become: yes
```

**这种设计的目的是：**

1. **全局操作**：执行不特定于某个角色的任务
2. **跨角色配置**：协调多个角色之间的设置
3. **环境特定任务**：针对特定环境的特殊处理
4. **简化角色设计**：保持角色的通用性和可重用性

**执行顺序：**
```
角色执行前任务 (pre_tasks) → 角色任务 → 角色执行后任务 (tasks) → 处理器 (handlers)
```

## 自定义模块 (custom_module.py) 详解

### 模块介绍

`library/custom_module.py` 是一个自定义 Ansible 模块示例，展示了如何扩展 Ansible 的功能。

### 模块结构

```python
#!/usr/bin/python3
from ansible.module_utils.basic import AnsibleModule

def main():
    # 1. 定义模块参数
    module = AnsibleModule(
        argument_spec=dict(
            message=dict(type='str', required=True),
            repeat=dict(type='int', default=1)
        )
    )
    
    # 2. 获取参数值
    message = module.params['message']
    repeat = module.params['repeat']
    
    # 3. 模块逻辑处理
    result = dict(
        changed=False,  # 表示模块是否改变了系统状态
        original_message=message,
        repeated_message=message * repeat,
        message="Task completed successfully"
    )
    
    # 4. 返回结果
    module.exit_json(**result)

if __name__ == '__main__':
    main()
```

### 各部分详解

#### 1. 参数定义 (`argument_spec`)
```python
argument_spec=dict(
    message=dict(type='str', required=True),  # 必需字符串参数
    repeat=dict(type='int', default=1)        # 可选整数参数，默认值1
)
```
- `type`: 参数数据类型（str, int, bool, list, dict等）
- `required`: 是否必需参数
- `default`: 默认值

#### 2. 参数获取
```python
message = module.params['message']
repeat = module.params['repeat']
```
- 通过 `module.params` 字典访问传入的参数

#### 3. 业务逻辑和结果构造
```python
result = dict(
    changed=False,  # 关键字段：是否改变了系统状态
    original_message=message,
    repeated_message=message * repeat,
    message="Task completed successfully"
)
```
- `changed`: **最重要的字段**，告诉 Ansible 系统状态是否改变
- 其他字段：自定义返回数据

#### 4. 结果返回
```python
module.exit_json(**result)  # 成功返回
# 或者 module.fail_json(msg="错误信息")  # 失败返回
```

### 在 Playbook 中的使用

```yaml
- name: 使用自定义模块
  hosts: all
  tasks:
    - name: 调用自定义模块
      custom_module:  # 模块名就是文件名（去掉.py）
        message: "Hello World"
        repeat: 3
      register: custom_result

    - name: 显示结果
      debug:
        var: custom_result
```

### 输出结果
```json
{
  "changed": false,
  "original_message": "Hello World",
  "repeated_message": "Hello WorldHello WorldHello World",
  "message": "Task completed successfully"
}
```

### 实际应用场景

1. **封装复杂逻辑**：将复杂的 shell 命令封装成模块
2. **API 集成**：与外部系统（云平台、监控系统）交互
3. **数据验证**：在模块内部进行参数验证和错误处理
4. **状态检查**：检查资源状态并返回是否需要变更

### 更实用的示例

```python
#!/usr/bin/python3
from ansible.module_utils.basic import AnsibleModule
import os

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', required=True),
            content=dict(type='str', required=True),
            backup=dict(type='bool', default=False)
        )
    )
    
    path = module.params['path']
    content = module.params['content']
    backup = module.params['backup']
    
    changed = False
    backup_path = None
    
    # 检查文件是否存在且内容是否相同
    if os.path.exists(path):
        with open(path, 'r') as f:
            current_content = f.read()
        if current_content != content:
            changed = True
            if backup:
                backup_path = path + '.backup'
                os.rename(path, backup_path)
    else:
        changed = True
    
    # 如果内容不同，写入新内容
    if changed:
        with open(path, 'w') as f:
            f.write(content)
    
    result = dict(
        changed=changed,
        path=path,
        backup_path=backup_path,
        message="File updated" if changed else "File already correct"
    )
    
    module.exit_json(**result)
```

这个自定义模块会：
- 检查文件内容是否需要更新
- 可选地创建备份
- 只在必要时更新文件（符合 Ansible 幂等性原则）

## 变量加载优先级

从高到低：
1. `host_vars/` 中的主机特定变量
2. `group_vars/` 中的组变量  
3. `roles/nginx/vars/main.yml` 角色变量
4. `roles/nginx/defaults/main.yml` 角色默认变量
5. `group_vars/all.yml` 全局变量

## 常用命令

```bash
# 语法检查
ansible-playbook --syntax-check site.yml

# 试运行（不实际执行）
ansible-playbook --check site.yml

# 实际运行
ansible-playbook site.yml

# 指定 inventory 运行
ansible-playbook -i inventory site.yml

# 只运行特定 tags
ansible-playbook site.yml --tags "nginx,config"

# 使用自定义模块
ansible all -m custom_module -a "message='Hello' repeat=3"
```

## 总结

这个结构提供了清晰的职责分离，使 Playbook 易于维护、扩展和重用。自定义模块功能展示了 Ansible 的强大扩展能力，可以根据具体需求创建专用的模块来简化复杂操作。
```

这个 README.md 文件完整地解释了项目结构、各个文件的作用，并特别详细介绍了自定义模块的内容和使用方法，同时说明了 MySQL 任务的作用和可移除性。
