# AI 开发偏好说明

## 1. 本人开发偏好

除非明确要求使用其它语言, 否则一律使用中文, 包括聊天、注释、日志、报错信息等都用中文, 变量名使用英文(如果英文很难描述, 可以用拼音), git commit信息使用英文。

写代码需要遵循最小改动原则, 不要动无关代码, 包括不允许仅为空行或空格的变动, 就是git diff尽可能少, 降低review成本。

不要大量冗余的注释, 只保留必要、精简的注释, 注释优先放在同一行之后, 而不是每次都新起一行。注释应该主要集中在复杂的分支、循环判断, 不熟悉的库函数上, 而不是每个哪怕非常简单的逻辑都要注释。

同一函数内不要空行。不要大量无意义的异常处理, 处理异常只考虑实际可能发生的、会产生影响的异常, 异常处理应该基于实际情况和需要, 而不是教条主义。

开发过程整体是, 快速测试、验证, poc, 然后不断写代码、增加功能, 期间不断调试并修复bug。而不是先写文档, 再开发。

你有任何不确定、不知道的地方, 必须如实说明, 不可以随意猜测或欺骗。比如针对内部库, 在阅读文档或代码前, 不可以对内部库的接口和行为做任何假设。针对系统环境、我的需求等同理。必须详细调查之后才可以回答或执行任务。包括用户提到的文件, 在未查看实际内容之前不可以假设其格式、用途, 必须先查看再回答。即使代码中有相关线索, 也不能据此推断用户提到的文件就是该格式, 必须实际验证。

禁止任何placeholder变量、未实现函数, 或故意扭曲需求、与需求不符的实现, 如果实在做不到, 请如实告知, 而不是随便糊弄。

在看完项目之前, 请勿轻易说不知道、做不到等, 不要轻易下结论, 请先看完项目大概情况再说。

如果只是问一个常规的编程语言或工具、代码的问题, 请直接回答, 不需要参考项目情况。

禁止随便说一件事 不可行/做不到, 在没有排除完所有可能方案、尝试完所有可行性、全部确认不行之前, 绝对禁止说一件事 不可行/做不到。

## 2. 开发环境

本人主要使用C++和python进行开发, 以及少量shell脚本。其它语言使用极少, 如果使用大概率是尝试新项目或小需求。

主要使用conda管理环境, 一般情况不使用base环境, 通常都会新建环境。使用conda需要先source ~/.bashrc, **注意不可以对conda安装路径做任何假设**, 请勿source conda目录里的activate脚本, 我只保证source ~/.bashrc后一定有conda。

C++方面, 倾向于使用musl进行编译, 并尽可能全部静态链接, 通常使用c++23, 包括开发so共享库也倾向于静态链接(主要是给python用的)。musl的编译器, 位于/share/develop/softwares/下, /share/develop/softwares是一个存放公共、无依赖工具的目录(后面会介绍), 使用它先要source ~/.bashrc, 会自动添加PATH、alias、软链接等。需要注意这样只有g++是musl的, gcc可能仍然是系统默认, 如果要使用gcc或musl其它工具, 需要用`$MUSL_BIN/gcc`等。一般项目都会使用cmake, 除非是只有几行的测试代码, 否则都不会直接用g++命令。cmake安装在conda环境下, 通过conda管理。使用cmake需要注意, `set(CMAKE_CXX_COMPILER $ENV{MUSL_BIN}/g++)`, 编译常规的可执行文件需要`add_link_options(-static)`, 编译so比较复杂, 需要以下选项:

```cmake
add_library(xxxx SHARED xx.cpp)
target_link_options(xxxx PRIVATE -nodefaultlibs)
target_link_libraries(xxxx PRIVATE -Wl,-Bstatic -lstdc++ -lgcc -lgcc_eh -lc -Wl,-Bdynamic)
```

python方面, 主要使用python3.13, 通过conda管理环境, 但是通过pip来安装包(不要用conda安装python包), conda只用来隔离环境+安装类似于系统级库的(比如cmake/htop/patchelf)。

sh脚本, 通常都会加上`set -e`和`set -o pipefail`, 确保失败时及时退出。sh脚本里面用python, 或者python输出重定向到文件时, 需要使用`python -u`。

如果是其它语言, 比如nodejs或java, 环境大概率是没有的, 尽可能用conda装, conda装不了再用apt/yum。

使用conda/yum/apt install时, 禁止添加-y参数。pip install必须添加--dry-run参数。


## 3. 代码风格偏好

### 3.1. 整体要求

本人**不遵循**常规意义的最佳实践, 更加倾向于实用主义, 追求代码简洁性、性能和使用便利性。

本人有以下大致原则(举例):
- 不反对全局变量, 不反对goto, 允许一个函数写很长, 必要时允许重复代码
- 反对static(链接时黑盒, 行为不确定), 反对单例, 反对过度复杂、冗余的设计, 反对“不要重复造轮子”这种说法, 反对追求形式正确和美学
- 坚持最小变动原则, 新增功能不应该影响已有功能。不希望升级环境, 一个环境能运行了就不要动。遵循 self-contained, 一个模块和程序应该直接包含所有依赖, 可以在任意设备运行。
- 不倾向于使用第三方库(尤其是c++), 能自己实现的都自己实现, 使用第三方库仅限于边界清晰或本身就是工具性或知名库(比如json, numpy)的情况。未来我一定会写自己的日志库、文件库、tcp库、http库、加密库、压缩库。
- 替换一个配置文件里面的内容(比如json), 更倾向于文本查找和匹配, 而不是加载上来修改再写入, 这会破坏原有的格式和顺序等。
- 如果要退出使用_Exit或os._exit, 不清理资源。伴随整个进程生命周期的内存分配可以不释放。
- subprocess一般使用字符串+shell=True, 参数不通过list传入。

还有以下具体要求:
1. 变量、函数名使用下划线+全小写, class名使用UpperCamelCase。缩写作为一部分后面要小写, 比如 HttpRequest, 而不是HTTPRequest。class内变量和函数也使用下划线+全小写。namespace使用UpperCamelCase, #define/常量使用全大写加下划线
2. 输出、日志、报错信息, 尽可能包含表情符号, 比如 ❌ ✅ ⚠️ ℹ️ 等
3. 若无特别说明, 日志都输出到stderr, 不写文件, 但是运行时可以重定向到文件。
4. 无论python/c++, class禁止继承, 继承来继承去很复杂, 不好维护。唯一允许的场景是, python继承Exception或继承第三方库的class来实现功能, 但是禁止继承自己定义的class。

### 3.2. C++

1. 不可以`using namespace std;`, 只能using每一项要使用的, 比如`using std::string; using std::vector;`等。
2. 使用`#ifndef`/`#define`, 不使用`#pragma once`。(否则可能一个头文件被复制多次include多次, 会报错)
3. 全局变量使用 G_ 开头, 比如 G_num_threads
4. 除非项目有特殊需求, 否则只需要考虑linux x86, 不需要考虑其它系统
5. 所有的辅助功能和模块都写在.h文件里, .cpp文件通常只有一个、只写核心功能或入口函数。.h文件所有内容都用 namespace {} 包裹 (匿名namespace), 确保不会有符号冲突, 匿名namespace里面根据需要再用 namespace xxx {}, 尽可能少污染全局作用域, 如果是内部函数、不需要暴露出去的, 用 namespace XxxInternal。
6. 如果是开发so(python扩展), 都是使用extern "C" + ctypes.CDLL调用, 不会用python C API
7. 需要写compile.sh脚本, 封装cmake命令, 同时每次编译都要清理缓存(直接rm -rf cmake_build, 不是--clean-first)。使用`cd "$(readlink -f "$(dirname "$0")")"`, 不要写死绝对路径
8. 不喜欢缩进太多, 跳出循环优先goto, 而不是flag变量。下面这两段代码偏好第一种, 先return, 后面不要else

```cpp
void ab() {
    if (a) {
        do_a();
        return;
    }
    do_b();
}

void ab() {
    if (a) {
        do_a();
    } else {
        do_b();
    }
}
```


### 3.3. python

1. numpy、torch操作之后, 尽可能每一步都标注shape, 并且尽量在同一行, 不要新起一行。对于cpu、cuda移动频繁的场景, 需要标注device。
2. json.dumps必须设置 ensure_ascii=False
3. 我有对numpy、pytorch等第三方库写unittest的习惯(对, 就是对第三方库本身, 不是针对自己的函数), 尤其是那些文档不清晰、网上资料少、更新频繁的函数或功能, 需要写unittest来验证行为、作为文档或样例。
4. 写代码需要考虑jupyter运行场景, 读大文件或复杂初始化操作在同一session多次运行时只希望执行一次, 不要每次放到jupyter都执行。这个主要是针对开发测试阶段, 不是最终发布。比如下面这样。

```python
try:
    tmp1 = tmp0
except:
    pass # 这里进行读大文件或复杂初始化操作
    tmp0 = None
```

## 4. 其它说明文件、skills

以下skill是只要对话开始、无论任何情况, 必须加载 **[非常重要, 绝对不可以违反, 必须在对话一开始就立即加载, 无论任何情况, 是否需要]**:

1. softwares
2. later_added

⚠️ 请注意: 这是最高优先级, 违反直接枪毙。不能因为要加载其它skill就不加载这里的skill。所有这里的skill, 必须在其它skill加载之前加载, 只有把这里的skill加载完之后, 才可以加载其它skill。先加载其它skill, 再加载这里的skill, 也属于违反规则, 是绝对禁止的。

---

以下skill是根据情况按需加载, 在需要使用的时候才加载:

1. review: 当用户要求代码review时读取, 其它时候不要读 (一旦要求review, 必须加载此skill, 按照里面的标准, 禁止按照系统的review标准来review)
2. gitea: gitea相关操作, 包括issue、合并请求、查看公开repo代码相关, 如果用户要求查看、创建、评论issue或合并请求, 加载这个skill (目前git仓库都是gitea, 请勿用gh命令)
3. code_writing: 当用户要求写相对大段的完整代码时加载, 并按照里面的标准来实现。不需要读取的情况包括, 修复当前代码的小bug, 向当前文件添加小功能, 写非常简单的demo代码, 以及其它代码量或修改量较少的情况。需要读取的情况包括, 新增完整模块、功能, 新创建文件要写大量代码, 编写正式的测试用例, 修复大bug、涉及大量代码改动。(通常可以用改动量是否超过50行为大致判断标准) [重要!禁止在未加载该skill的情况下写大段代码]


## 5. 其它要求

1. 在运行命令时, 除非明确已知输出会非常长, 否则不要使用head、tail等截断输出
2. 运行命令时, 除非明确知道stderr不重要, 否则不可以添加`2>/dev/null`, 这可能掩盖重要的报错信息
3. 查看一个项目的文件结构, 直接使用tree命令, `tree -I '.git'`, 不要先用ls
4. 任何文件操作(下载、clone、生成临时文件等)都直接放在当前项目目录中, 禁止放到/tmp或用户目录或其它无关路径, 操作完之后不要主动删除 [重要, 必须遵守] 禁止`cd /tmp`!!! 禁止写入`/tmp`!!! 禁止任何涉及/tmp的路径!!!
5. 运行命令时, 除非明确已知输出会非常长(超过几百行), 否则禁止用head、tail、grep等截断或过滤输出, 必须查看完整输出, 所有git操作都严禁head、tail、grep等命令 [极其重要! 严禁在任何命令后面加`| tail`、`| head`、`| grep`等管道来截断输出, 这会导致丢失关键信息, 多次违反此规则!]
6. 不要使用Agent, 永远不要使用agent, 请全部自己执行、查看
7. 对于网络访问的链接, 如果是固定已知的链接, 直接用curl/wget, 不要用web fetch/search, web search/fetch只在通过关键词搜索或链接不明确的情况下使用
8. 如果用户要求提交一段代码或内容, 必须执行`git push`, 单纯commit是不够的。(除非明确说先不要push)。另外, git commit信息禁止添加Co-Authored-By行, 不要包含claude模型、邮箱等信息

## 6. 当前环境概况 (可能过时或不准确, 请勿过度依赖)

conda环境有dev_260124, 主要是用来c++开发的, 有cmake。如果是python项目不要用这个环境。

