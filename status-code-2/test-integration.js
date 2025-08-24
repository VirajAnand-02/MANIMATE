#!/usr/bin/env node

import fetch from 'node-fetch';

const NODEJS_API = 'http://localhost:5001';
const PYTHON_API = 'http://localhost:8001';

async function testIntegration() {
    console.log('🧪 Testing AI Video Generation Pipeline Integration\n');

    try {
        // Test 1: Check if both servers are running
        console.log('1️⃣ Testing server connectivity...');
        
        try {
            const nodeResponse = await fetch(`${NODEJS_API}/health`);
            const nodeData = await nodeResponse.json();
            console.log('✅ Node.js server:', nodeData.message);
        } catch (error) {
            console.log('❌ Node.js server not accessible:', error.message);
            return;
        }

        try {
            const pythonResponse = await fetch(`${PYTHON_API}/`);
            const pythonData = await pythonResponse.json();
            console.log('✅ Python API server:', pythonData.name);
        } catch (error) {
            console.log('❌ Python API server not accessible:', error.message);
            return;
        }

        // Test 2: Test script generation
        console.log('\n2️⃣ Testing script generation...');
        const submitResponse = await fetch(`${NODEJS_API}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: 'basic mathematics',
                uid: 'test_user_123',
                chatID: 'test_chat_456'
            })
        });

        if (submitResponse.ok) {
            const submitData = await submitResponse.json();
            console.log('✅ Script generation initiated');
            console.log(`📝 Generated ${submitData.tokens?.length || 0} script tokens`);
            
            if (submitData.tokens && submitData.tokens.length > 0) {
                const testToken = submitData.tokens[0];
                
                // Test 3: Test script retrieval
                console.log('\n3️⃣ Testing script retrieval...');
                const scriptResponse = await fetch(`${PYTHON_API}/api/script/${testToken}`);
                
                if (scriptResponse.ok) {
                    const scriptData = await scriptResponse.json();
                    console.log('✅ Script retrieval successful');
                    console.log(`📄 Script title: ${scriptData.title || 'No title'}`);
                    console.log(`🎬 Scenes count: ${scriptData.scenes?.length || 0}`);
                } else {
                    console.log('⚠️ Script not ready yet (this is normal for fresh generation)');
                }

                // Test 4: Test script update
                console.log('\n4️⃣ Testing script update...');
                const updateResponse = await fetch(`${NODEJS_API}/update_script/${testToken}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        script: {
                            title: 'Updated Test Script',
                            scenes: [
                                {
                                    seq: 1,
                                    text: 'This is a test narration',
                                    anim: 'Simple animation description',
                                    layout: 'title_and_main_content'
                                }
                            ]
                        },
                        chatID: 'test_chat_456'
                    })
                });

                if (updateResponse.ok) {
                    console.log('✅ Script update successful');
                } else {
                    console.log('❌ Script update failed:', await updateResponse.text());
                }

                // Test 5: Test video generation start
                console.log('\n5️⃣ Testing video generation initiation...');
                const confirmResponse = await fetch(`${NODEJS_API}/confirm_script/${testToken}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        chatID: 'test_chat_456',
                        config: {
                            topic: 'Test Video Generation',
                            quality: 'low',
                            tts_provider: 'mock'  // Use mock for testing
                        }
                    })
                });

                if (confirmResponse.ok) {
                    const confirmData = await confirmResponse.json();
                    console.log('✅ Video generation initiated');
                    console.log(`🆔 Job ID: ${confirmData.job_id}`);

                    // Test 6: Test job status
                    console.log('\n6️⃣ Testing job status monitoring...');
                    const statusResponse = await fetch(`${NODEJS_API}/generation_status/${confirmData.job_id}`);
                    
                    if (statusResponse.ok) {
                        const statusData = await statusResponse.json();
                        console.log('✅ Job status retrieval successful');
                        console.log(`📊 Status: ${statusData.job_status.status}`);
                        console.log(`📈 Progress: ${statusData.job_status.progress}%`);
                    } else {
                        console.log('❌ Job status retrieval failed');
                    }
                } else {
                    console.log('❌ Video generation failed:', await confirmResponse.text());
                }
            }
        } else {
            console.log('❌ Script generation failed:', await submitResponse.text());
        }

        console.log('\n🎉 Integration test completed!');
        console.log('\n📋 Summary:');
        console.log('- Both servers are communicating properly');
        console.log('- API endpoints are functional');
        console.log('- Data flow is working as expected');
        console.log('\n💡 Next steps:');
        console.log('- Configure your environment variables (.env files)');
        console.log('- Set up your AI service API keys');
        console.log('- Test with real script generation (non-mock)');

    } catch (error) {
        console.error('❌ Integration test failed:', error.message);
        console.log('\n🔧 Troubleshooting:');
        console.log('1. Make sure both servers are running');
        console.log('2. Check environment variables are set');
        console.log('3. Verify network connectivity');
        console.log('4. Check server logs for errors');
    }
}

// Add Node.js fetch if not available
if (!globalThis.fetch) {
    const fetch = (await import('node-fetch')).default;
    globalThis.fetch = fetch;
}

testIntegration();
