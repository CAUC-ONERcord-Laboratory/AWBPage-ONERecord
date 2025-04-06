document.addEventListener('DOMContentLoaded', function() {
    // DOM元素集合
    const DOM = {
        container: document.querySelector('.container'),
        waybillContainer: document.querySelector('.waybill-container'),
        toggleBtn: document.querySelector('.toggle-btn'),
        submitBtn: document.querySelector('.submit-btn'),
        iframe: document.querySelector('.waybill-container iframe'),
        userInput: document.getElementById('user-input')
    };

    // 添加调试代码
    console.log('DOM Elements:', DOM);
    window.waybillIframe = DOM.iframe;
    
    if (!DOM.toggleBtn) {
        console.error('Toggle button not found!');
        return;
    }

    // 提交功能
    DOM.submitBtn?.addEventListener('click', async () => {
        try {
            if (!window.waybillIframe) {
                throw new Error('请等待运单框架加载完成');
            }

            const rawData = DOM.userInput.value.trim();
            if (!rawData) return alert('请输入数据');
            
            const jsonData = JSON.parse(rawData);
            const apiResponse = await fetch('http://localhost:5000/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ waybill: jsonData })
            });

            if (!apiResponse.ok) throw new Error('请求失败');
            
            fillWaybillData(await apiResponse.json());
            toggleView(true);
            
        } catch (error) {
            alert(`操作失败: ${error.message}`);
            console.error(error);
        }
    });

    // 视图切换
    DOM.toggleBtn?.addEventListener('click', (e) => {
        console.log('Toggle button clicked!'); 
        e.preventDefault(); // 防止事件冒泡
        toggleView();
    });

    // 视图控制函数
    function toggleView(expand) {
        console.log('Toggle view called, current state:', DOM.container.classList.contains('collapsed')); // 添加调试日志
        const isExpanded = expand ?? !DOM.container.classList.contains('collapsed'); 
        console.log('Will expand to:', isExpanded); // 添加调试日志
        
        // 强制触发重排
        DOM.container.style.display = 'flex';
        DOM.waybillContainer.style.display = 'block';
        
        // 设置类名
        DOM.container.classList.toggle('collapsed', isExpanded);
        DOM.waybillContainer.classList.toggle('expanded', isExpanded);
        DOM.toggleBtn.innerHTML = isExpanded ? '≫':'≪'  ;
        
        // 打印当前状态
        console.log('Classes after toggle:', {
            container: DOM.container.className,
            waybill: DOM.waybillContainer.className
        });
    }
});

// 直接填充函数
function fillWaybillData(data) {
    const iframe = window.waybillIframe;
    if (!iframe) throw new Error('运单框架未加载');
    const doc = iframe.contentDocument || iframe.contentWindow.document;

    // 数据-元素ID映射配置
    const DATA_MAPPING = {
        // 发货人信息
        'Shipper.Name': 'shipperName',
        'Shipper.Address': 'shipperAddress',
        
        // 收货人信息
        'Consignee.Name': 'consigneeName',
        'Consignee.Address': 'consigneeAddress',
        
        // 航空公司信息
        'Issued_by.Name': 'issued_byName',
        'Issued_by.Airlinecode': 'issued_byAirlinecode',
        'Issuing_Carrier_Agent': 'issuing_carrier_agent',

        'Accounting_Information': 'accounting_information',
        // # # #航班信息
        'To': 'to',
        'Airport_of_Departure': 'airport_of_departure',
        'First_Carrier': 'first_carrier',
        'Airport_of_Destination': 'airport_of_destination',
        'Flight': 'flight',
        'Date': 'date',
        'WT_VAL': 'wt_val',
        'Other': 'other',
        'Declared_Value_For_Carriage.Value': 'declared_value_for_carriage_value',
        'Declared_Value_For_Customs.Value': 'declared_value_for_customs_value',
        'Amount_of_Insurance.Value': 'amount_of_insurance_value',
        'Total_Gross_Weight': 'total_gross',
        "Total_Chargeable_Weight": "total_chargeable",
        'Rate_Charge.Value': 'rate_charge_value',


        // Other_Charges
        // Other_Charges
        // Other_Charges
        // Other_Charges
        // Other_Charges
        // Other_Charges
        // Other_Charges
        // Other_Charges
        // Other_Charges
        // Other_Charges


        'Signature_of_Shipper_or_his_Agent':'signature_of_shipper_or_his_agent',
        'Signature_of_Carrier_or_its_Agent':'signature_of_carrier_or_its_agent',
        'Executed_Date':'executed_date',
        'Executed_Place': 'executed_place',
        'No_of_Pieces': 'no_of_pieces',
        'Total_Dimensions': 'total_dimensions',
        'Total_Goods_Descriptions': 'total_goods_descriptions',



    };

    // 通用填充方法
    Object.entries(DATA_MAPPING).forEach(([dataPath, elementId]) => {
        const element = doc.getElementById(elementId);
        let value = getNestedValue(data, dataPath) || '';
    
        // 转换对象为字符串
        if (value && typeof value === 'object') {
            value = Object.values(value)
                .filter(v => v != null)
                .join(', ');
        }
    
        const DEFAULT_VALUES = {
            'amount_of_insurance_value': 'NIL',
            'declared_value_for_carriage_value': 'NVD',
            'declared_value_for_customs_value': 'NCV'
        };
        value = value || DEFAULT_VALUES[elementId] || value;
    
        if (element) {
            element.value = value; // 确保是字符串
            triggerChange(element);
        }
    });
}

// 辅助函数：安全获取嵌套对象值
function getNestedValue(obj, path) {
    return path.split('.').reduce((o, p) => (o || {})[p], obj);
}

// 辅助函数：触发变更事件
function triggerChange(element) {
    element.dispatchEvent(new Event('change', { bubbles: true }));
}

