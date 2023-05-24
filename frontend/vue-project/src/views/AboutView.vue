<template>
  <div class="wrap">
    <div class="item">
      <div class="ava">
        <div>
          <h2>Backend developer - Sergey Makshakov</h2>
          <p>Email: sejey44@gmail.com</p>
          <p>Telegram is my preferred messenger: https://t.me/serj_chat</p>
        </div>

        <v-avatar size="130">
          <img src="../assets/ava-130x141.jpg" alt="Serj" />
        </v-avatar>
      </div>
      <hr />
      <h3>Hello. I am grateful for your attention.</h3>
      <p>I have an engineering degree in computer science and 18 years of experience in the IT sphere.</p>
      <div class="pl">
        <ul>
          <li>For the last 4 years I've been working as a programmer, primarily as a backend developer. During this time I gained good experience with Python and JavaScript, as well as a good understanding of databases such as MongoDB and PostgreSQL.</li>
          <li>5 years of freelance and owner of a web studio. I dealt with internet marketing and web development.</li>
          <li>I worked as a system administrator for 9 years. Setting up servers and virtualisation.</li>
        </ul>
      </div>
      <p>
        <b>Worked in professional fields:</b> IT outsourcing, IT systems integration, industrial production, medicine, tourism, hotel business, railway transport.
      </p>  
      <p>
        <b>Hobbies:</b> oil painting, sports (basketball, swimming, windsurfing) and trying to read books, which are too difficult for me).
      </p>
    </div>
  </div>
</template>

<style scoped>
.wrap {
  /* display: flex; */
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  line-height: 40px;
}
.item {
  text-align: left;
}
.ava {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
hr {
  margin: 20px 0;
}
.pl {
  padding-left: 40px;
}
</style>