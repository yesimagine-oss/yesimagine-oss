package main

import (
	"fmt"
	"os"

	"github.com/openclaw/go-image-skill/internal/cli"
)

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	command := os.Args[1]
	args := os.Args[2:]

	switch command {
	case "analyze":
		if len(args) < 1 {
			fmt.Println("错误：请提供图片路径")
			fmt.Println("用法：image-skill analyze <图片路径> [查询]")
			os.Exit(1)
		}
		query := ""
		if len(args) > 1 {
			query = args[1]
		}
		cli.Analyze(args[0], query)

	case "batch":
		if len(args) < 1 {
			fmt.Println("错误：请提供目录路径")
			fmt.Println("用法：image-skill batch <目录路径>")
			os.Exit(1)
		}
		cli.Batch(args[0])

	case "query":
		if len(args) < 2 {
			fmt.Println("错误：请提供查询和图片路径")
			fmt.Println("用法：image-skill query <查询> <图片路径>")
			os.Exit(1)
		}
		cli.Query(args[0], args[1])

	case "serve":
		cli.Serve(args)

	case "search":
		if len(args) < 2 {
			fmt.Println("错误：请提供查询词和目录路径")
			fmt.Println("用法：image-skill search <查询词> <目录路径>")
			os.Exit(1)
		}
		cli.Search(args[0], args[1])

	case "compare":
		if len(args) < 2 {
			fmt.Println("错误：请提供两张图片路径")
			fmt.Println("用法：image-skill compare <图片 1> <图片 2>")
			os.Exit(1)
		}
		cli.Compare(args[0], args[1])

	case "version":
		fmt.Println("go-image-skill v1.0.0")

	case "help", "-h", "--help":
		printUsage()

	default:
		fmt.Printf("未知命令：%s\n", command)
		printUsage()
		os.Exit(1)
	}
}

func printUsage() {
	fmt.Println(`Go Image Skill - 全能型图像分析工具

用法:
  image-skill <命令> [参数]

命令:
  analyze <图片路径> [查询]     分析单张图片
  batch <目录路径>              批量分析目录中的图片
  query <查询> <图片路径>        自然语言查询图片
  serve [选项]                  启动 HTTP API 服务
  search <查询词> <目录路径>     搜索图片
  compare <图片 1> <图片 2>      比对两张图片
  version                       显示版本信息
  help                          显示帮助信息

示例:
  image-skill analyze photo.jpg
  image-skill analyze photo.jpg "照片里有几个人？"
  image-skill batch ./photos/
  image-skill query "有猫吗？" photo.jpg
  image-skill serve --port 8080
  image-skill search "海边" ./photos/
  image-skill compare photo1.jpg photo2.jpg`)
}
