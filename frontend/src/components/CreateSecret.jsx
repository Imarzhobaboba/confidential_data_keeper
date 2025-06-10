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
      const data = {
        secret: values.secret,
        ttl_seconds: values.ttl_seconds || 3600, // Дефолтное значение 1 час
      };
      
      const result = await api.createSecret(data);
      setAccessKey(result.access_key);
      message.success('Secret created successfully!');
      form.resetFields();
    } catch (error) {
      message.error(`Error: ${error.message}`);
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
        >
          <InputNumber 
            min={1} 
            style={{ width: '100%' }} 
            placeholder="3600 (1 hour)" 
          />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
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