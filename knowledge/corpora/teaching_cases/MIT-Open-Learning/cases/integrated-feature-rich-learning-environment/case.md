> 检索摘要：该材料匹配电气工程与计算机科学（Course 6）高阶研讨课（6.042, 6.046, 6.849, 6.854）的同步协作教学主题，教学问题在于远程环境下模拟物理空间中的灵活分组、即时助教响应与协同记录。对象为上述课程学生，情境为远程同步问题解决与办公时间。实施策略由Erik Demaine开发并部署开源三件套：Comingle（虚拟会议室系统）、Coauthor（实时协同笔记）、Cocreate（共享虚拟白板）。工具明确列出Flexible Course Delivery与Remote Teaching。评价方式未陈述具体评估机制，但效果包括成功复现物理教室多房间配置逻辑、支持手举队列调度助教访问、实现笔记与草图实时同步，并形成可嵌入Zoom/Jitsi/CoCalc等任意iframe应用的‘universal glue’式集成环境。

- Source: https://openlearning.mit.edu/mit-faculty/residential-digital-innovations/integrated-feature-rich-learning-environment
- source_format: html
- capture_date: 2026-10-09

---

# An Integrated, Feature-rich Learning Environment

6.042, 6.046, 6.849, 6.854 Electrical Engineering & Computer Science (Course 6)     ![MIT Prof Erik Demaine](https://openlearning.mit.edu/sites/default/files/styles/event_news_detail/public/residential-innovations/Erik_Demaine-web.jpg?itok=9-0pUhEr)       Faculty/Instructor  Erik Demaine    Digital Innovations & Tools  Flexible Course Delivery Remote Teaching

Professor Erik Demaine has developed a three-part software suite that offers a wide range of new functionalities for synchronous interactions with students:

- [Comingle](https://github.com/edemaine/comingle): a web conferencing platform that provides enhanced spaces for virtual meetings.
- [Coauthor](https://github.com/edemaine/coauthor): a collaborative software application that allows students to record notes, discussions, ideas, and results in the moment and in a shared space.
- [Cocreate](https://github.com/edemaine/cocreate): a shared virtual whiteboard.

Demaine and his staff use Comingle for virtual synchronous problem solving, and other classes use it for office hours. Students are able to talk with each other as well as be visited by course staff. In addition, Comingle replicates the configuration that was used when the class met in physical space: course staff would reserve multiple classrooms next to each other, and students could go to different rooms depending on what problems they were working on. Comingle simulates this in a virtual environment: each virtual room has a name, a video instance, and a digital whiteboard. From any virtual room, a student can raise their hand if they want to request being visited by staff. Raised hands from all the rooms form a queue which course staff can refer to in order to see who's been waiting the longest.

Coauthor and Cocreate function as components that enhance Comingle, or can be used separately. With Coauthor, multiple users can write notes at the same time with instant live synchronization. Students can edit the same post at the same time, and add images. As students formulate ideas and prototypes, Cocreate lets them immediately sketch them on a virtual whiteboard.

The flexibility and adaptability of Comingle renders it a “universal glue”. It is possible to embed Zoom or Jitsi Meet video calls, different whiteboard tools, clicker.mit, a Google document, CoCalc, Slides.com, and any other application that can be iframed.

The integrated suite of Comingle, Coauthor, and Cocreate presents a flexible, integrated, feature-rich learning environment where students and course staff can seamlessly meet, learn, discuss, work, communicate, and collaborate. All of the tools are freely available and open source and can be adapted to one's needs. To learn more: [github.com/edemaine/cosuite/](https://github.com/edemaine/cosuite/).

Back to [Residential Digital Innovations](https://openlearning.mit.edu/mit-faculty/residential-digital-innovations).
