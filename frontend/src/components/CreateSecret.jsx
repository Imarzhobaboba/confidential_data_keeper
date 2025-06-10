import React, { useState } from 'react';
import { Button, Form, Input, InputNumber, message } from 'antd';
import { CopyOutlined } from '@ant-design/icons';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import api from '../api';

const CreateSecret = () => {
  const [form] = Form.useForm();
  const [accessKey, setAccessKey] = useState(null);
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      // Дополнительная проверка (на случай, если валидация формы не сработала)
      const ttl = parseInt(values.ttl_seconds, 10);
      if (isNaN(ttl)) {
        throw new Error('Invalid lifetime value');
      }

      const data = {
        secret: values.secret,
        ttl_seconds: ttl, // гарантированно число
      };
      
      const result = await api.createSecret(data);
      
      if (!result?.access_key) {
        throw new Error('Invalid server response');
      }
      
      setAccessKey(result.access_key);
      message.success('Secret created successfully!');
      form.resetFields();
    } catch (error) {
      console.error('Error creating secret:', error);
      
      // Специальная обработка для 422 ошибки (невалидные данные)
      if (error.response?.status === 422) {
        const serverErrors = error.response.data?.detail || {};
        let errorMsg = 'Validation error';
        
        if (Array.isArray(serverErrors)) {
          errorMsg = serverErrors.map(e => e.msg).join(', ');
        } else if (typeof serverErrors === 'string') {
          errorMsg = serverErrors;
        }
        
        message.error(`Server validation error: ${errorMsg}`);
        return;
      }
      
      message.error(`Failed to create secret: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Form
        form={form}
        layout="vertical"
        onFinish={onFinish}
        initialValues={{ ttl_seconds: 3600 }}
        onFinishFailed={({ errorFields }) => {
          // Показываем первую ошибку валидации
          message.error(errorFields[0].errors[0]);
        }}
      >
        <Form.Item
          name="secret"
          label="Your Secret"
          rules={[{ required: true, message: 'Please enter your secret' }]}
        >
          <Input.TextArea rows={4} placeholder="Enter your sensitive data here" />
        </Form.Item>

        <Form.Item
          name="ttl_seconds"
          label="Lifetime (seconds)"
          tooltip="Time after which the secret will be automatically deleted"
          extra="Must be a whole number between 1 and 31536000 (1 year)"
          rules={[
            { required: true, message: 'Please enter lifetime in seconds' },
            () => ({
              validator(_, value) {
                // Проверяем, что значение - целое число
                if (!/^\d+$/.test(value)) {
                  return Promise.reject('Must be a whole number');
                }
                
                const num = parseInt(value, 10);
                
                if (num < 1) {
                  return Promise.reject('Must be at least 1 second');
                }
                
                if (num > 31536000) {
                  return Promise.reject('Maximum is 31536000 seconds (1 year)');
                }
                
                return Promise.resolve();
              },
            }),
          ]}
        >
          <Input 
            placeholder="3600 (1 hour)"
            // Запрещаем ввод чего-либо кроме цифр
            onKeyPress={(e) => {
              if (!/[0-9]/.test(e.key)) {
                e.preventDefault();
              }
            }}
          />
        </Form.Item>

        <Form.Item>
          <Button 
            type="primary" 
            htmlType="submit" 
            loading={loading}
            onClick={() => {
              // Дополнительная валидация перед отправкой
              form.validateFields()
                .catch(() => {
                  message.error('Please fix the errors in the form');
                });
            }}
          >
            Create Secret
          </Button>
        </Form.Item>
      </Form>

      {accessKey && (
        <div style={{ marginTop: '20px' }}>
          <h4>Access Key:</h4>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <Input 
              value={accessKey} 
              readOnly 
              style={{ marginRight: '8px' }} 
            />
            <CopyToClipboard 
              text={accessKey} 
              onCopy={() => message.success('Copied to clipboard!')}
            >
              <Button icon={<CopyOutlined />}>Copy</Button>
            </CopyToClipboard>
          </div>
          <p style={{ color: '#ff4d4f', marginTop: '8px' }}>
            ⚠️ Save this key! You won't be able to retrieve the secret without it.
          </p>
        </div>
      )}
    </div>
  );
};

export default CreateSecret;