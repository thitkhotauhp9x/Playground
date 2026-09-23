import { Container, Grid, Skeleton } from '@mantine/core';
import { Calendar } from '@mantine/dates';
import {QA} from "@/app/components/questions/QA";

const child = <Skeleton height={140} radius="md" animate={false} />;

export function GridAsymmetrical() {
  return (
    <Container my="md">
      <Grid>
        <Grid.Col span={{ base: 12, xs: 4 }}>
          <Calendar/>
          {child}
        </Grid.Col>
        <Grid.Col span={{ base: 12, xs: 8 }}>
          <QA></QA>
          {child}
        </Grid.Col>
        {/*<Grid.Col span={{ base: 12, xs: 8 }}>{child}</Grid.Col>*/}
        {/*<Grid.Col span={{ base: 12, xs: 4 }}>{child}</Grid.Col>*/}
        {/*<Grid.Col span={{ base: 12, xs: 3 }}>{child}</Grid.Col>*/}
        {/*<Grid.Col span={{ base: 12, xs: 3 }}>{child}</Grid.Col>*/}
        {/*<Grid.Col span={{ base: 12, xs: 6 }}>{child}</Grid.Col>*/}
      </Grid>
    </Container>
  );
}
