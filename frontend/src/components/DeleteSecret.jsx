import React, { useState } from 'react';
import { Button, Form, Input, Modal, message } from 'antd';
import api from '../api';

const DeleteSecret = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);

  const onFinish = async (values) => {
    setIsModalVisible(true);
  };

  const handleDelete = async () => {
    setLoading(true);
    try {
      const accessKey = form.getFieldValue('access_key');
      const success = await api.deleteSecret(accessKey);
      
      if (success) {
        message.success('Secret deleted successfully!');
        form.resetFields();
      }
    } catch (error) {
      message.error(`Error: ${error.message}`);
    } finally {
      setLoading(false);
      setIsModalVisible(false);
    }
  };

  return (
    <div>
      <Form form={form} layout="vertical" onFinish={onFinish}>
        <Form.Item
          name="access_key"
          label="Access Key"
          rules={[{ required: true, message: 'Please enter access key' }]}
        >
          <Input placeholder="Enter access key to delete" />
        </Form.Item>

        <Form.Item>
          <Button type="primary" danger htmlType="submit">
            Delete Secret
          </Button>
        </Form.Item>
      </Form>

      <Modal
        title="Confirm Deletion"
        visible={isModalVisible}
        onOk={handleDelete}
        onCancel={() => setIsModalVisible(false)}
        confirmLoading={loading}
      >
        <p>Are you sure you want to permanently delete this secret?</p>
        <p style={{ color: '#ff4d4f' }}>
          ⚠️ This action cannot be undone!
        </p>
      </Modal>
    </div>
  );
};

export default DeleteSecret;