document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.container');
    const waybillContainer = document.querySelector('.waybill-container');
    const toggleBtn = document.querySelector('.toggle-btn');
    const submitBtn = document.querySelector('.submit-btn');
    const iframe = document.querySelector('.waybill-container iframe');
    const userInput = document.getElementById('user-input');

    console.log('Elements found:', {
        container: !!container,
        waybillContainer: !!waybillContainer,
        toggleBtn: !!toggleBtn,
        submitBtn: !!submitBtn,
        iframe: !!iframe,
        userInput: !!userInput
    });

    // 等待 iframe 加载完成
    if (iframe) {
        iframe.addEventListener('load', function() {
            console.log('Iframe loaded successfully');
            window.waybillIframe = iframe;
        });
    }

    // 提交按钮点击事件
    if (submitBtn) {
        submitBtn.addEventListener('click', async function() {
            console.log('Submit button clicked');
            try {
                // 获取用户输入
                const inputValue = userInput.value.trim();
                if (!inputValue) {
                    alert('请输入数据');
                    return;
                }

                console.log('User input:', inputValue);

                // 解析输入数据
                let jsonData;
                try {
                    jsonData = JSON.parse(inputValue);
                } catch (e) {
                    alert('请输入有效的 JSON 数据');
                    return;
                }

                // 调用 API
                const response = await fetch('http://localhost:5000/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        waybill: jsonData
                    })
                });

                const data = await response.json();
                console.log('API response:', data);

                if (!response.ok) {
                    throw new Error(data.error || '请求失败');
                }

                // 填充数据到运单
                await fillWaybillData(data);

                // 切换视图
                container.classList.add('collapsed');
                waybillContainer.classList.add('expanded');
                toggleBtn.innerHTML = '≪';

            } catch (error) {
                console.error('Error:', error);
                alert('错误: ' + error.message);
            }
        });
    }

    // 切换按钮点击事件
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            console.log('Toggle button clicked');
            
            // 检查当前状态并切换
            if (container.classList.contains('collapsed')) {
                // 如果已经折叠，则展开
                container.classList.remove('collapsed');
                waybillContainer.classList.remove('expanded');
                toggleBtn.innerHTML = '≫';
                console.log('Expanding container');
            } else {
                // 如果已经展开，则折叠
                container.classList.add('collapsed');
                waybillContainer.classList.add('expanded');
                toggleBtn.innerHTML = '≪';
                console.log('Collapsing container');
            }
        });
    }
});

async function fillWaybillData(data) {
    console.log('Filling waybill data:', data);
    
    if (!data || !data.Shipper || !data.Consignee) {
        console.error('Invalid data format:', data);
        throw new Error('数据格式不正确');
    }

    const iframe = window.waybillIframe;
    if (!iframe) {
        console.error('Iframe not found');
        throw new Error('找不到运单框架');
    }

    try {
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        console.log('Accessing iframe document');

        // 查找所有输入框
        const inputs = Array.from(iframeDoc.querySelectorAll('input[type="text"]'));
        console.log('Found inputs:', inputs.length);

        // 查找并填充发货人信息
        let shipperFound = false;
        let consigneeFound = false;

        inputs.forEach((input, index) => {
            const prevElement = input.previousElementSibling;
            if (prevElement) {
                if (prevElement.textContent.includes("Shipper's Name and Address")) {
                    if (!shipperFound) {
                        input.value = data.Shipper.Name;
                        if (inputs[index + 1]) {
                            inputs[index + 1].value = data.Shipper.Address;
                        }
                        shipperFound = true;
                        console.log('Shipper info filled');
                    }
                } else if (prevElement.textContent.includes("Consignee's Name and Address")) {
                    if (!consigneeFound) {
                        input.value = data.Consignee.Name;
                        if (inputs[index + 1]) {
                            inputs[index + 1].value = data.Consignee.Address;
                        }
                        consigneeFound = true;
                        console.log('Consignee info filled');
                    }
                }
            }
        });

        if (!shipperFound) {
            console.error('Could not find shipper input fields');
        }
        if (!consigneeFound) {
            console.error('Could not find consignee input fields');
        }

        // 触发 change 事件
        inputs.forEach(input => {
            if (input.value) {
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });

    } catch (error) {
        console.error('Error filling waybill:', error);
        throw new Error('填充运单时出错: ' + error.message);
    }
}

