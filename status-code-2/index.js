import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import path from "path";
import {setChatDB, updateChatDB} from "./functions/db.js";
import {
  streamVideo,
  getVideoInfo,
  listVideos,
  validateVideoFile,
} from "./functions/vdo_stream.js";
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001;

// Store active SSE connections
const sseClients = new Map();

// Middleware
app.use(express.json());
app.use(cors());

// SSE endpoint for real-time script updates
app.get("/events/:chatID", (req, res) => {
  const {chatID} = req.params;

  // Set SSE headers
  res.writeHead(200, {
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Cache-Control",
  });

  // Store client connection
  sseClients.set(chatID, res);
  console.log(`SSE client connected: ${chatID}`);

  // Send initial connection message
  res.write(
    `data: ${JSON.stringify({
      type: "connected",
      message: "Connected to script updates",
      timestamp: new Date().toISOString(),
    })}\n\n`
  );

  // Handle client disconnect
  req.on("close", () => {
    console.log(`SSE client disconnected: ${chatID}`);
    sseClients.delete(chatID);
  });
});

// Function to send script to specific client
function sendScriptToClient(
  chatID,
  scriptData,
  readyToken,
  scriptIndex,
  totalScripts
) {
  const client = sseClients.get(chatID);
  if (client) {
    try {
      client.write(
        `data: ${JSON.stringify({
          type: "script_ready",
          data: scriptData,
          readyToken: readyToken,
          scriptIndex: scriptIndex,
          totalScripts: totalScripts,
          timestamp: new Date().toISOString(),
        })}\n\n`
      );
      console.log(`Sent script ${scriptIndex} to client: ${chatID}`);
      return true;
    } catch (error) {
      console.error(`Error sending script to client ${chatID}:`, error);
      sseClients.delete(chatID);
      return false;
    }
  } else {
    console.warn(`Client ${chatID} not found in active connections`);
    return false;
  }
}

// Function to send completion message
function sendCompletionToClient(chatID, allScripts, allTokens) {
  const client = sseClients.get(chatID);
  if (client) {
    try {
      client.write(
        `data: ${JSON.stringify({
          type: "all_scripts_complete",
          allScripts: allScripts,
          allTokens: allTokens,
          timestamp: new Date().toISOString(),
        })}\n\n`
      );
      console.log(`Sent completion message to client: ${chatID}`);
    } catch (error) {
      console.error(`Error sending completion to client ${chatID}:`, error);
      sseClients.delete(chatID);
    }
  }
}

// VIDEO STREAMING ENDPOINTS

// Get list of available videos
app.get("/videos", (req, res) => {
  try {
    const videos = listVideos();
    res.status(200).json({
      success: true,
      videos: videos,
      count: videos.length,
    });
  } catch (error) {
    console.error("Error listing videos:", error);
    res.status(500).json({
      success: false,
      message: "Error retrieving video list",
    });
  }
});

// Get video metadata
app.get("/video-info/:filename", (req, res) => {
  try {
    const {filename} = req.params;
    const validation = validateVideoFile(filename);

    if (!validation.valid) {
      return res.status(404).json({
        success: false,
        message: validation.error,
      });
    }

    const videoInfo = getVideoInfo(validation.path);

    if (!videoInfo.exists) {
      return res.status(404).json({
        success: false,
        message: "Video file not found",
      });
    }

    res.status(200).json({
      success: true,
      video: videoInfo,
    });
  } catch (error) {
    console.error("Error getting video info:", error);
    res.status(500).json({
      success: false,
      message: "Error retrieving video information",
    });
  }
});

// Stream video with range support
app.get("/stream/:filename", (req, res) => {
  try {
    const {filename} = req.params;
    console.log(`Streaming request for: ${filename}`);

    // Validate the video file
    const validation = validateVideoFile(filename);

    if (!validation.valid) {
      return res.status(404).json({
        success: false,
        message: validation.error,
      });
    }

    // Stream the video
    streamVideo(req, res, validation.path);
  } catch (error) {
    console.error("Error streaming video:", error);
    res.status(500).json({
      success: false,
      message: "Error streaming video",
    });
  }
});

// Serve static video files (alternative method)
app.get("/download/:filename", (req, res) => {
  try {
    const {filename} = req.params;
    const validation = validateVideoFile(filename);

    if (!validation.valid) {
      return res.status(404).json({
        success: false,
        message: validation.error,
      });
    }

    // Set headers for download
    res.setHeader("Content-Disposition", `attachment; filename="${filename}"`);
    res.setHeader("Content-Type", "video/mp4");

    // Send file
    res.sendFile(validation.path);
  } catch (error) {
    console.error("Error downloading video:", error);
    res.status(500).json({
      success: false,
      message: "Error downloading video",
    });
  }
});

// POST endpoint to receive text and uid, start script generation
app.post("/submit", async (req, res) => {
  try {
    const {text, uid, chatID} = req.body;

    // Validate required fields
    if (!text || !uid || !chatID) {
      return res.status(400).json({
        success: false,
        message: "Text, UID, and ChatID are required",
      });
    }

    console.log(`Received request from ${uid}: ${text}`);

    // Generate script tokens from Python API
    const responseScript = await fetch(process.env.PYTHON_API_URL + "/api/generate_scripts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        topic: text,
        quality: "high",
        tts_provider: "gemini",
        voice: "Kore",
        enable_parallel: true,
        max_tts_workers: 4,
        max_render_workers: 2,
        use_thinking: true,
        use_batch: true
      }),
    });

    if (!responseScript.ok) {
      throw new Error(`Python API error: ${responseScript.status} ${responseScript.statusText}`);
    }

    const scriptData = await responseScript.json();
    const {tokens} = scriptData;

    // Handle token as array - ensure we have exactly 3 tokens
    const tokenArray = Array.isArray(tokens) ? tokens : [tokens];
    console.log(`Generated script tokens for ${uid}:`, tokenArray);

    // Initialize database with empty scripts array
    const dbSts = await setChatDB({
      uid: uid,
      text: text,
      script: null,
      scriptToken: tokenArray,
      readyToken: null,
      chatID: chatID,
    });

    if (dbSts && dbSts.success === false) {
      return res.status(500).json({
        success: false,
        message: "Error saving to database",
      });
    }

    // Poll for all scripts synchronously, then respond
    const maxPolls = 600; // 60 * 10s = 600s
    const completedScripts = [];
    const completedTokens = [];
    const pollingStatus = tokenArray.map(() => ({
      completed: false,
      data: null,
    }));

    for (let pollCount = 0; pollCount < maxPolls; pollCount++) {
      // Check if all scripts are completed
      if (pollingStatus.every((status) => status.completed)) {
        break;
      }

      await new Promise((resolve) => setTimeout(resolve, 10000));

      try {
        // Poll each token that hasn't completed yet
        const pollPromises = tokenArray.map(async (token, index) => {
          if (pollingStatus[index].completed) {
            return null;
          }
          try {
            const pollResponse = await fetch(
              `${process.env.PYTHON_API_URL}/api/script/${token}`
            );
            const pollData = await pollResponse.json();
            if (pollData && pollData.scenes && pollData.scenes.length > 0) {
              return {index, token, data: pollData};
            }
            return null;
          } catch (error) {
            console.error(`Error polling token ${token}:`, error);
            return null;
          }
        });

        const pollResults = await Promise.all(pollPromises);
        for (const result of pollResults) {
          if (result && !pollingStatus[result.index].completed) {
            pollingStatus[result.index].completed = true;
            pollingStatus[result.index].data = result.data;
            completedScripts[result.index] = result.data;
            completedTokens[result.index] = result.token;
            // Update database with the new script
            try {
              await updateChatDB({
                chatID: chatID,
                script: completedScripts.filter(Boolean),
                readyToken: completedTokens.filter(Boolean),
              });
            } catch (dbError) {
              console.error("Error updating database:", dbError);
            }
          }
        }
      } catch (pollError) {
        console.error("Error during polling:", pollError);
      }
    }

    // After polling, check if all scripts are ready
    if (pollingStatus.every((status) => status.completed)) {
      return res.status(200).json({
        success: true,
        message: "All scripts generated successfully",
        scripts: completedScripts,
        tokens: completedTokens,
        chatID: chatID,
      });
    } else {
      return res.status(202).json({
        success: false,
        message: "Timeout: Not all scripts were generated in time",
        scripts: completedScripts.filter(Boolean),
        tokens: completedTokens.filter(Boolean),
        chatID: chatID,
      });
    }
  } catch (error) {
    console.error("Error processing request:", error);
    res.status(500).json({
      success: false,
      message: "Internal server error",
    });
  }
});

// Background function to poll all scripts and stream results
async function pollAllScripts(tokenArray, chatID, uid, text) {
  const maxPolls = 600; // 60 * 10s = 600s
  const completedScripts = [];
  const completedTokens = [];
  const pollingStatus = tokenArray.map(() => ({completed: false, data: null}));

  console.log(`Starting background polling for ${tokenArray.length} scripts`);

  // Poll continuously until all scripts are ready or timeout
  for (let pollCount = 0; pollCount < maxPolls; pollCount++) {
    console.log(`Polling attempt ${pollCount + 1}/${maxPolls}`);

    // Check if all scripts are completed
    if (pollingStatus.every((status) => status.completed)) {
      console.log("All scripts completed!");
      break;
    }

    await new Promise((resolve) => setTimeout(resolve, 10000));

    try {
      // Poll each token that hasn't completed yet
      const pollPromises = tokenArray.map(async (token, index) => {
        if (pollingStatus[index].completed) {
          return {
            index,
            token,
            data: null,
            ready: false,
            alreadyCompleted: true,
          };
        }

        try {
          const pollResponse = await fetch(
            `${process.env.PYTHON_API_URL}/api/script/${token}`
          );
          const pollData = await pollResponse.json();

          // Check if this token's script is ready
          if (pollData && pollData.scenes && pollData.scenes.length > 0) {
            return {
              index,
              token,
              data: pollData,
              ready: true,
              alreadyCompleted: false,
            };
          }
          return {
            index,
            token,
            data: pollData,
            ready: false,
            alreadyCompleted: false,
          };
        } catch (error) {
          console.error(`Error polling token ${token}:`, error);
          return {
            index,
            token,
            data: null,
            ready: false,
            alreadyCompleted: false,
          };
        }
      });

      const pollResults = await Promise.all(pollPromises);

      // Process newly completed scripts
      for (const result of pollResults) {
        if (result.ready && !result.alreadyCompleted) {
          const {index, token, data} = result;

          // Mark as completed
          pollingStatus[index].completed = true;
          pollingStatus[index].data = data;

          // Add to completed arrays
          completedScripts.push(data);
          completedTokens.push(token);

          console.log(`Script ${index + 1} completed for token: ${token}`);

          // Send this script to the client immediately
          sendScriptToClient(chatID, data, token, index + 1, tokenArray.length);

          // Update database with the new script
          try {
            await updateChatDB({
              chatID: chatID,
              script: completedScripts,
              readyToken: completedTokens,
            });
          } catch (dbError) {
            console.error("Error updating database:", dbError);
          }
        }
      }
    } catch (pollError) {
      console.error("Error during polling:", pollError);
    }
  }

  // Send final completion message
  if (completedScripts.length > 0) {
    sendCompletionToClient(chatID, completedScripts, completedTokens);
  }

  console.log(
    `Polling completed. Generated ${completedScripts.length}/${tokenArray.length} scripts`
  );
}

// Health check endpoint
app.get("/health", (req, res) => {
  res.status(200).json({
    success: true,
    message: "Server is running",
    timestamp: new Date().toISOString(),
  });
});

// Update script endpoint - forwards script updates to Python API
app.post("/update_script/:token", async (req, res) => {
  try {
    const {token} = req.params;
    const {script, chatID} = req.body;

    if (!script || !chatID) {
      return res.status(400).json({
        success: false,
        message: "Script data and ChatID are required",
      });
    }

    console.log(`Updating script for token: ${token}`);

    // Forward script update to Python API
    const updateResponse = await fetch(
      `${process.env.PYTHON_API_URL}/api/script/${token}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(script),
      }
    );

    if (!updateResponse.ok) {
      throw new Error(`Python API error: ${updateResponse.status} ${updateResponse.statusText}`);
    }

    const updateData = await updateResponse.json();

    // Update database with the new script
    try {
      await updateChatDB({
        chatID: chatID,
        script: [updateData.script],
        readyToken: [token],
      });
    } catch (dbError) {
      console.error("Error updating database:", dbError);
      return res.status(500).json({
        success: false,
        message: "Script updated in Python API but failed to update database",
      });
    }

    res.status(200).json({
      success: true,
      message: "Script updated successfully",
      script: updateData.script,
      token: token,
    });

  } catch (error) {
    console.error("Error updating script:", error);
    res.status(500).json({
      success: false,
      message: "Error updating script",
      error: error.message,
    });
  }
});

// Confirm script and start video generation
app.post("/confirm_script/:token", async (req, res) => {
  try {
    const {token} = req.params;
    const {chatID, config} = req.body;

    if (!chatID) {
      return res.status(400).json({
        success: false,
        message: "ChatID is required",
      });
    }

    console.log(`Starting video generation for token: ${token}`);

    // Start video generation via Python API
    const generationResponse = await fetch(
      `${process.env.PYTHON_API_URL}/api/generate/${token}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(config || {
          topic: "Generated Video",
          quality: "high",
          tts_provider: "gemini",
          voice: "Kore",
          enable_parallel: true,
          max_tts_workers: 4,
          max_render_workers: 2,
          use_thinking: true,
          use_batch: true
        }),
      }
    );

    if (!generationResponse.ok) {
      throw new Error(`Python API error: ${generationResponse.status} ${generationResponse.statusText}`);
    }

    const generationData = await generationResponse.json();

    res.status(200).json({
      success: true,
      message: "Video generation started successfully",
      job_id: generationData.job_id,
      status: generationData.status,
      token: token,
      chatID: chatID,
    });

  } catch (error) {
    console.error("Error starting video generation:", error);
    res.status(500).json({
      success: false,
      message: "Error starting video generation",
      error: error.message,
    });
  }
});

// Check video generation progress
app.get("/generation_status/:job_id", async (req, res) => {
  try {
    const {job_id} = req.params;

    console.log(`Checking generation status for job: ${job_id}`);

    // Check job status via Python API
    const statusResponse = await fetch(
      `${process.env.PYTHON_API_URL}/api/job/${job_id}`
    );

    if (!statusResponse.ok) {
      if (statusResponse.status === 404) {
        return res.status(404).json({
          success: false,
          message: "Job not found",
        });
      }
      throw new Error(`Python API error: ${statusResponse.status} ${statusResponse.statusText}`);
    }

    const statusData = await statusResponse.json();

    res.status(200).json({
      success: true,
      job_status: statusData,
    });

  } catch (error) {
    console.error("Error checking generation status:", error);
    res.status(500).json({
      success: false,
      message: "Error checking generation status",
      error: error.message,
    });
  }
});

// List all generation jobs
app.get("/generation_jobs", async (req, res) => {
  try {
    const {limit = 50} = req.query;

    console.log(`Fetching generation jobs (limit: ${limit})`);

    // Get jobs list via Python API
    const jobsResponse = await fetch(
      `${process.env.PYTHON_API_URL}/api/jobs?limit=${limit}`
    );

    if (!jobsResponse.ok) {
      throw new Error(`Python API error: ${jobsResponse.status} ${jobsResponse.statusText}`);
    }

    const jobsData = await jobsResponse.json();

    res.status(200).json({
      success: true,
      jobs: jobsData.jobs,
      total: jobsData.total,
    });

  } catch (error) {
    console.error("Error fetching generation jobs:", error);
    res.status(500).json({
      success: false,
      message: "Error fetching generation jobs",
      error: error.message,
    });
  }
});

// Delete a generation job
app.delete("/generation_job/:job_id", async (req, res) => {
  try {
    const {job_id} = req.params;

    console.log(`Deleting generation job: ${job_id}`);

    // Delete job via Python API
    const deleteResponse = await fetch(
      `${process.env.PYTHON_API_URL}/api/job/${job_id}`,
      {
        method: "DELETE",
      }
    );

    if (!deleteResponse.ok) {
      if (deleteResponse.status === 404) {
        return res.status(404).json({
          success: false,
          message: "Job not found",
        });
      }
      throw new Error(`Python API error: ${deleteResponse.status} ${deleteResponse.statusText}`);
    }

    const deleteData = await deleteResponse.json();

    res.status(200).json({
      success: true,
      message: deleteData.message,
    });

  } catch (error) {
    console.error("Error deleting generation job:", error);
    res.status(500).json({
      success: false,
      message: "Error deleting generation job",
      error: error.message,
    });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Available endpoints:`);
  console.log(`  GET    /health - Health check`);
  console.log(`  GET    /videos - List available videos`);
  console.log(`  GET    /video-info/:filename - Get video metadata`);
  console.log(`  GET    /stream/:filename - Stream video with range support`);
  console.log(`  GET    /download/:filename - Download video file`);
  console.log(
    `  GET    /events/:chatID - SSE connection for real-time script updates`
  );
  console.log(
    `  POST   /submit - Submit text, uid, chatID to start script generation`
  );
  console.log(
    `  POST   /update_script/:token - Update script via Python API`
  );
  console.log(
    `  POST   /confirm_script/:token - Confirm script and start video generation`
  );
  console.log(
    `  GET    /generation_status/:job_id - Check video generation progress`
  );
  console.log(
    `  GET    /generation_jobs - List all generation jobs`
  );
  console.log(
    `  DELETE /generation_job/:job_id - Delete a generation job`
  );
  console.log(`\nMake sure to set PYTHON_API_URL environment variable to point to the Python API server`);
  console.log(`Example: PYTHON_API_URL=http://localhost:8001`);
});
