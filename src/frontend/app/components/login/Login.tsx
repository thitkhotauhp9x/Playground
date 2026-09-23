import { useDisclosure } from "@mantine/hooks";
import { Modal, Button, TextInput, PasswordInput } from "@mantine/core";
import React from "react";

export function Login() {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Modal opened={opened} onClose={close} title="Authentication">
        <TextInput label="Email" placeholder="you@mantine.dev" required />
        <PasswordInput
          label="Mật khẩu"
          placeholder="Mật khẩu của bạn"
          required
        />

        <Button type="submit" fullWidth mt="xl">
          Đăng nhập
        </Button>
      </Modal>

      <Button variant="default" onClick={open}>
        Login
      </Button>
    </>
  );
}
