"use client";

import { useState } from 'react';
import { Button, Code, Text, TextInput } from '@mantine/core';
import { hasLength, isEmail, useForm } from '@mantine/form';
import {InputWithButton} from "@/app/components/conversation/InputWithButton";

export function Demo() {
  const form = useForm({
    mode: 'controlled',
    initialValues: { name: '', email: '' },
    validate: {
      name: hasLength({ min: 3 }, 'Must be at least 3 characters'),
      email: isEmail('Invalid email'),
    },
  });

  const [submittedValues, setSubmittedValues] = useState<typeof form.values | null>(null);

  return (
      <>
        <form onSubmit={form.onSubmit(setSubmittedValues)}>
          <TextInput {...form.getInputProps('name')} label="Name" placeholder="Name" />
          <TextInput {...form.getInputProps('email')} mt="md" label="Email" placeholder="Email" />
          <Button type="submit" mt="md">
            Submit
          </Button>

          <Text mt="md">Form values:</Text>
          <Code block>{JSON.stringify(form.values, null, 2)}</Code>

          <Text mt="md">Submitted values:</Text>
          <Code block>{submittedValues ? JSON.stringify(submittedValues, null, 2) : '–'}</Code>
        </form>
    </>
  );
}