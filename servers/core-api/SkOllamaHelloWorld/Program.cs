// 引入必要的命名空间
using Microsoft.SemanticKernel;
using System.Text;

// --- Step 1: 设置Ollama的连接信息 ---
// Ollama暴露的API端点，通常是这个地址。
// 如果你的Ollama在不同的机器或端口上，请修改这里。
string ollamaEndpoint = "http://localhost:57572";

// 你想使用的本地模型名称，必须是你已经用 `ollama pull` 下载好的。
// 例如: "llama3", "mistral", "qwen2", "gemma:2b"
string modelId = "gpt-oss:20b";

Console.OutputEncoding = Encoding.UTF8; // 确保终端能正确显示中文等字符
Console.WriteLine("✨ Semantic Kernel is calling local Ollama...");

// --- Step 2: 构建Kernel ---
// Kernel是Semantic Kernel的核心，是所有AI功能的“大脑中枢”。
var builder = Kernel.CreateBuilder();

// 添加一个实现了IChatCompletionService的服务。
// 我们使用AddOpenAIChatCompletion，因为它与Ollama的API格式兼容。
builder.AddOpenAIChatCompletion(
    modelId: modelId,                // 指定要使用的模型
    endpoint: new Uri(ollamaEndpoint), // 指定Ollama的API地址
    apiKey: "ollama");               // 对于Ollama，apiKey可以是任意非空字符串

// 从builder构建出Kernel实例
var kernel = builder.Build();

Console.WriteLine($"✅ Kernel configured for model: {modelId}");

// --- Step 3: 准备你的第一个Prompt ---
// 这是一个简单的“内联”Prompt。
// {{$input}} 是一个模板变量，我们稍后会填充它。
string promptTemplate = @"
你是一个充满激情的游戏开发者，你的项目DreamWorld刚刚启动。
请为你的项目写一句充满力量和梦想的开场白。
主题是：{{$input}}
";

// 创建一个KernelFunction，让SK知道这是一个可以执行的Prompt
var dreamWorldIntroFunction = kernel.CreateFunctionFromPrompt(promptTemplate);

// --- Step 4: 执行Prompt并获取结果 ---
Console.WriteLine("\n🚀 Invoking the prompt...");

// 调用Kernel的InvokeAsync方法来执行我们的函数
// 使用KernelArguments来安全地传递输入变量
var result = await kernel.InvokeAsync(
    dreamWorldIntroFunction,
    new() {
        { "input", "AI驱动的无限流世界" } // 填充prompt模板中的 {{$input}}
    });

// --- Step 5: 显示结果 ---
Console.WriteLine("\n🎉 Ollama's Response:\n--------------------");
Console.WriteLine(result);
Console.WriteLine("--------------------");

// 等待用户按键退出，以便查看结果
Console.ReadKey();