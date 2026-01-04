#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const TODOIST_API_TOKEN = process.env.TODOIST_API_TOKEN;
const BASE_URL = "https://api.todoist.com/rest/v2";

if (!TODOIST_API_TOKEN) {
  console.error("Error: TODOIST_API_TOKEN environment variable is required");
  process.exit(1);
}

// Helper function for API calls
async function todoistApi(endpoint, method = "GET", body = null) {
  const options = {
    method,
    headers: {
      Authorization: `Bearer ${TODOIST_API_TOKEN}`,
      "Content-Type": "application/json",
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, options);

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Todoist API error (${response.status}): ${error}`);
  }

  // Some endpoints return 204 No Content
  if (response.status === 204) {
    return { success: true };
  }

  return response.json();
}

// Create the server
const server = new Server(
  {
    name: "todoist-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "todoist_list_projects",
        description: "List all projects in Todoist",
        inputSchema: {
          type: "object",
          properties: {},
          required: [],
        },
      },
      {
        name: "todoist_list_tasks",
        description:
          "List tasks from Todoist. Can filter by project_id or get all active tasks.",
        inputSchema: {
          type: "object",
          properties: {
            project_id: {
              type: "string",
              description: "Optional project ID to filter tasks",
            },
            filter: {
              type: "string",
              description:
                "Optional Todoist filter query (e.g., 'today', 'overdue', 'p1')",
            },
          },
          required: [],
        },
      },
      {
        name: "todoist_create_task",
        description: "Create a new task in Todoist",
        inputSchema: {
          type: "object",
          properties: {
            content: {
              type: "string",
              description: "The task content/title",
            },
            description: {
              type: "string",
              description: "Optional task description",
            },
            project_id: {
              type: "string",
              description: "Optional project ID (defaults to Inbox)",
            },
            due_string: {
              type: "string",
              description:
                "Natural language due date (e.g., 'tomorrow', 'next monday', 'Jan 15')",
            },
            priority: {
              type: "number",
              description: "Priority from 1 (normal) to 4 (urgent)",
              enum: [1, 2, 3, 4],
            },
            labels: {
              type: "array",
              items: { type: "string" },
              description: "Array of label names to apply",
            },
          },
          required: ["content"],
        },
      },
      {
        name: "todoist_complete_task",
        description: "Mark a task as complete",
        inputSchema: {
          type: "object",
          properties: {
            task_id: {
              type: "string",
              description: "The ID of the task to complete",
            },
          },
          required: ["task_id"],
        },
      },
      {
        name: "todoist_update_task",
        description: "Update an existing task",
        inputSchema: {
          type: "object",
          properties: {
            task_id: {
              type: "string",
              description: "The ID of the task to update",
            },
            content: {
              type: "string",
              description: "New task content/title",
            },
            description: {
              type: "string",
              description: "New task description",
            },
            due_string: {
              type: "string",
              description: "New due date in natural language",
            },
            priority: {
              type: "number",
              description: "New priority (1-4)",
              enum: [1, 2, 3, 4],
            },
          },
          required: ["task_id"],
        },
      },
      {
        name: "todoist_delete_task",
        description: "Delete a task permanently",
        inputSchema: {
          type: "object",
          properties: {
            task_id: {
              type: "string",
              description: "The ID of the task to delete",
            },
          },
          required: ["task_id"],
        },
      },
      {
        name: "todoist_get_task",
        description: "Get details of a specific task by ID",
        inputSchema: {
          type: "object",
          properties: {
            task_id: {
              type: "string",
              description: "The ID of the task to retrieve",
            },
          },
          required: ["task_id"],
        },
      },
      {
        name: "todoist_search_tasks",
        description:
          "Search for tasks using a text query. Searches task content and descriptions.",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Text to search for in tasks",
            },
          },
          required: ["query"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "todoist_list_projects": {
        const projects = await todoistApi("/projects");
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(projects, null, 2),
            },
          ],
        };
      }

      case "todoist_list_tasks": {
        let endpoint = "/tasks";
        const params = new URLSearchParams();

        if (args?.project_id) {
          params.append("project_id", args.project_id);
        }
        if (args?.filter) {
          params.append("filter", args.filter);
        }

        if (params.toString()) {
          endpoint += `?${params.toString()}`;
        }

        const tasks = await todoistApi(endpoint);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(tasks, null, 2),
            },
          ],
        };
      }

      case "todoist_create_task": {
        const taskData = {
          content: args.content,
        };

        if (args.description) taskData.description = args.description;
        if (args.project_id) taskData.project_id = args.project_id;
        if (args.due_string) taskData.due_string = args.due_string;
        if (args.priority) taskData.priority = args.priority;
        if (args.labels) taskData.labels = args.labels;

        const task = await todoistApi("/tasks", "POST", taskData);
        return {
          content: [
            {
              type: "text",
              text: `Task created successfully:\n${JSON.stringify(task, null, 2)}`,
            },
          ],
        };
      }

      case "todoist_complete_task": {
        await todoistApi(`/tasks/${args.task_id}/close`, "POST");
        return {
          content: [
            {
              type: "text",
              text: `Task ${args.task_id} marked as complete!`,
            },
          ],
        };
      }

      case "todoist_update_task": {
        const updateData = {};
        if (args.content) updateData.content = args.content;
        if (args.description) updateData.description = args.description;
        if (args.due_string) updateData.due_string = args.due_string;
        if (args.priority) updateData.priority = args.priority;

        const task = await todoistApi(
          `/tasks/${args.task_id}`,
          "POST",
          updateData
        );
        return {
          content: [
            {
              type: "text",
              text: `Task updated:\n${JSON.stringify(task, null, 2)}`,
            },
          ],
        };
      }

      case "todoist_delete_task": {
        await todoistApi(`/tasks/${args.task_id}`, "DELETE");
        return {
          content: [
            {
              type: "text",
              text: `Task ${args.task_id} deleted permanently.`,
            },
          ],
        };
      }

      case "todoist_get_task": {
        const task = await todoistApi(`/tasks/${args.task_id}`);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(task, null, 2),
            },
          ],
        };
      }

      case "todoist_search_tasks": {
        // Get all tasks and filter locally (Todoist REST API doesn't have direct search)
        const tasks = await todoistApi("/tasks");
        const query = args.query.toLowerCase();
        const filtered = tasks.filter(
          (task) =>
            task.content.toLowerCase().includes(query) ||
            (task.description && task.description.toLowerCase().includes(query))
        );

        return {
          content: [
            {
              type: "text",
              text:
                filtered.length > 0
                  ? JSON.stringify(filtered, null, 2)
                  : `No tasks found matching "${args.query}"`,
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Todoist MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});






